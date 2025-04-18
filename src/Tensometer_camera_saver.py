import cv2
import os

# Proces zapisu klatek
def frame_saver(queue, folder):
    frame_count = 0
    while True:
        frame = queue.get()
        if frame is None:
            break
        cv2.imwrite(os.path.join(folder, f"frame_{frame_count:05d}.png"), frame)
        frame_count += 1