import cv2
import numpy as np

cam = cv2.VideoCapture("Lane_Detection_Test_Video_01.mp4")

top_left = (0, 0)
top_right = (0, 0)
bottom_left = (0, 0)
bottom_right = (0, 0)

previous_left_top_x = 0
previous_left_bottom_x = 0
previous_right_top_x = 0
previous_right_bottom_x = 0

fps = cam.get(cv2.CAP_PROP_FPS)
print(fps)

while True:
    ret, frame = cam.read()
    if ret is False:
        break

    # 2.Resize the frame to
    height, width = frame.shape[:2]
    new_width = round(width * 0.3)
    new_height = round(height * 0.3)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    cv2.imshow("Sezised", resized_frame)

    #3.Convert to grayscale
    gray_recolor = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale", gray_recolor)

    #4.Show only the road
    trapezoid_frame = np.zeros((new_height, new_width), dtype = np.uint8)

    lower_left = (0, new_height)
    lower_right = (new_width, new_height)
    upper_left = (round(new_width * 0.46), round(new_height * 0.75))
    upper_right = (round(new_width * 0.54), round(new_height * 0.75))
    trapezoid_bounds = np.array([upper_right, upper_left, lower_left, lower_right], dtype=np.float32)

    cv2.fillConvexPoly(trapezoid_frame, np.int32([trapezoid_bounds]), 1)
    trapezoid_frame = trapezoid_frame * gray_recolor

    cv2.imshow("Only road", trapezoid_frame)

    #5. Get a top down view
    frame_bounds = np.array([[new_width, 0], [0, 0], [0, new_height], [new_width, new_height]], dtype=np.float32)
    perspective_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, frame_bounds)
    top_down_frame = cv2.warpPerspective(trapezoid_frame, perspective_matrix, (new_width, new_height))
    cv2.imshow("Top down", top_down_frame)

    #6. Apply a blur filter
    blurred_frame = cv2.blur(top_down_frame, (7, 7), 0)
    cv2.imshow("Blurred", blurred_frame)

    #7. Apply Sobel filter

    sobel_vertical = np.float32([[-1,-2,-1],[0,0,0],[1,2,1]])
    sobel_horizontal = np.transpose(sobel_vertical)

    sobel_frame = np.float32(blurred_frame)
    sobel_frame2 = np.float32(blurred_frame)

    sobel_x = cv2.filter2D(sobel_frame, -1, sobel_horizontal)
    sobel_y = cv2.filter2D(sobel_frame2, -1, sobel_vertical)

    sobel_combined = np.sqrt(sobel_x**2 + sobel_y**2)
    cv2.imshow("Sobel", sobel_combined)

    #8. Apply binary
    _, binary_frame = cv2.threshold(sobel_combined, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow("Binary", binary_frame)

    #9. Get coordinates of the lane
    copy_frame = binary_frame.copy()
    copy_frame[:, :round(new_width * 0.05)] = 0
    copy_frame[:, round(new_width * 0.95):] = 0

    left_half = copy_frame[:, :new_width // 2]
    right_half = copy_frame[:, new_width // 2:]

    left_y, left_x = np.argwhere(left_half > 0).T
    right_y, right_x = np.argwhere(right_half > 0).T

    right_x += round(new_width * 0.5)

    #Find the lines
    left_b, left_a = np.polynomial.polynomial.polyfit(left_x, left_y, 1)
    right_b,right_a = np.polynomial.polynomial.polyfit(right_x, right_y, 1)

    #Find the points
    left_top_y = 0
    left_top_x = int(round((left_top_y - left_b) // left_a))
    if abs(left_top_x) >= 10**8:
        left_top_x = previous_left_top_x
    else:
        previous_left_top_x = left_top_x

    left_bottom_y = new_height
    left_bottom_x = int(round((left_bottom_y - left_b) // left_a))
    if abs(left_bottom_x) >= 10**8:
        left_bottom_x = previous_left_bottom_x
    else:
        previous_left_bottom_x = left_bottom_x

    right_top_y = 0
    right_top_x = int(round((right_top_y - right_b) // right_a))
    if abs(right_top_x) >= 10**8:
        right_top_x = previous_right_top_x
    else:
        previous_right_top_x = right_top_x

    right_bottom_y = new_height
    right_bottom_x = int(round((right_bottom_y - right_b) // right_a))
    if abs(right_bottom_x) >= 10**8:
        right_bottom_x = previous_right_bottom_x
    else:
        previous_right_bottom_x = right_bottom_x

    left_top = left_top_x, left_top_y
    left_bottom = left_bottom_x, left_bottom_y
    right_top = right_top_x, right_top_y
    right_bottom = right_bottom_x, right_bottom_y

    cv2.line(copy_frame, left_top, left_bottom, (200, 0, 0), thickness=5)
    cv2.line(copy_frame, right_top, right_bottom, (100, 0, 0), thickness=5)


    # Draw the vertical line separating the two halves
    cv2.line(copy_frame, (new_width // 2, 0), (new_width // 2, new_height), (255, 0, 0), thickness=1)
    cv2.imshow("Lane", copy_frame)

    #11. Final visualization

    blank_frame = np.zeros((new_height, new_width), dtype = np.uint8)
    cv2.line(blank_frame, left_top, left_bottom, (255, 0, 0), thickness=3)
    perspective = cv2.getPerspectiveTransform(frame_bounds, trapezoid_bounds)
    final_frame = cv2.warpPerspective(blank_frame, perspective, (new_width, new_height))
    cv2.imshow("Final_left", final_frame)
    left_y, left_x = np.argwhere(final_frame > 0).T


    blank_frame2 = np.zeros((new_height, new_width), dtype = np.uint8)
    cv2.line(blank_frame2, right_top, right_bottom, (255, 0, 0), thickness=3)
    final_frame2 = cv2.warpPerspective(blank_frame2, perspective, (new_width, new_height))
    cv2.imshow("Final_right", final_frame2)
    right_y, right_x = np.argwhere(final_frame2 > 0).T

    frame_copy = resized_frame.copy()
    for x, y in zip(left_x, left_y):
        frame_copy[y, x] = (250, 0, 250)

    # Color the pixels at the coordinates of the right line in green
    for x, y in zip(right_x, right_y):
        frame_copy[y, x] = (0, 250, 0)

    cv2.imshow("Final", frame_copy)

    if cv2.waitKey(1) == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
