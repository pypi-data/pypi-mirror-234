import cv2
import numpy as np

"""
ModifiedWay : 이미지 파일을 원하는 각도로 회전하는데, 원본 이미지를 자르지 않는 상태에서 회전하므로,
이미지가 작아지거나 커질 수 있다.
따라서 이 함수는 보통 원본 이미지가 주석의 ROI 박스와 이미지가 큰 차이가 없는 경우만 사용하는 것이 좋다.
왜냐하면 xml 주석의 크기를 결정하기가 쉽지 않기 때문이다.
Usage:
angles = [23, 45, 68, 90, 113, 135, 158, 180, 203, 226, 248, 270, 292, 315, 337]
            for angle in angles:
                () # 이미지 angle 처리
                modified_with_rotation_img = ModifiedWay(img, angle)
"""

def ModifiedWay(rotateImage, angle):
    # Taking image height and width
    imgHeight, imgWidth = rotateImage.shape[0], rotateImage.shape[1]

    # Computing the centre x,y coordinates
    # of an image
    centreY, centreX = imgHeight // 2, imgWidth // 2

    # Computing 2D rotation Matrix to rotate an image
    rotationMatrix = cv2.getRotationMatrix2D((centreY, centreX), angle, 1.0)

    # Now will take out sin and cos values from rotationMatrix
    # Also used numpy absolute function to make positive value
    cosofRotationMatrix = np.abs(rotationMatrix[0][0])
    sinofRotationMatrix = np.abs(rotationMatrix[0][1])

    # Now will compute new height & width of
    # an image so that we can use it in
    # warpAffine function to prevent cropping of image sides
    newImageHeight = int((imgHeight * sinofRotationMatrix) +
                         (imgWidth * cosofRotationMatrix))
    newImageWidth = int((imgHeight * cosofRotationMatrix) +
                        (imgWidth * sinofRotationMatrix))

    # After computing the new height & width of an image
    # we also need to update the values of rotation matrix
    rotationMatrix[0][2] += (newImageWidth / 2) - centreX
    rotationMatrix[1][2] += (newImageHeight / 2) - centreY

    # Now, we will perform actual image rotation
    rotatingimage = cv2.warpAffine(
        rotateImage, rotationMatrix, (newImageWidth, newImageHeight))

    return rotatingimage

"""
rotate_bound:
원하는 각도만큼 회전한 새로운 이미지를 만들고, 회전 메트릭스를 리턴받음.
그런데 만들어진 이미지의 scale은 그대로이므로, 이미지가 잘린 부분이 있을 수 있음.
Usage:
                M, modified_with_rotation_img = rotate_bound(img, angle)
"""
def rotate_bound(image, angle):
    # 이미지의 크기와 중심점 계산
    (h, w) = image.shape[:2]
    (cX, cY) = ((w - 1) // 2.0, (h - 1) // 2.0)

    # 회전 행렬 계산
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # 회전된 이미지의 크기 계산
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # 회전 행렬에 이동 변환 추가
    M[0, 2] += ((nW - 1) / 2.0) - cX
    M[1, 2] += ((nH - 1) / 2.0) - cY

    # 이미지 회전
    return M, cv2.warpAffine(image, M, (nW, nH))

"""
rotated_coord : 입력된 좌표 (x,y)의 회전된 새로운 좌표를 얻음.
새로 구한 좌표가 rotate_bound() 함수에서 얻은 이미지의 실제 좌표와 일치할지는 아직 테스트하지 못함.

Usage:
new_left_top = rotated_coord(old_left_top, M)
                
"""
# 좌표 회전 함수
def rotated_coord(points, M):
    points = np.array(points)
    ones = np.ones(shape=(len(points),1))
    points_ones = np.concatenate((points,ones), axis=1)
    transformed_pts = M.dot(points_ones.T).T
    return transformed_pts

# 입력된 scale(float) 만큼을 높이와 폭에 적용하여 변경된 이미지를 리턴한다.
def scale_image_change(img_path, scale):
    image = cv2.imread(img_path)

    changed_image = None
    if image is not None:
        h, w, c = image.shape
        to_scale = float(scale)
        scaled_h = int(h * to_scale)
        scaled_w = int(w * to_scale)
        if to_scale > 1.0:
            changed_image = cv2.resize(image, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
        else:
            changed_image = cv2.resize(image, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_AREA)

    return changed_image