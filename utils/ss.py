import sys
import cv2


def selective_search(im, ss_type='f', new_height=200):
    """
    selective search with opencv
    :param im:
    :param ss_type:
    :param new_height:
    :return:
    """
    # speed-up using multithreads
    cv2.setUseOptimized(True)
    cv2.setNumThreads(4)

    # resize image
    new_width = int(im.shape[1] * 200 / im.shape[0])
    im = cv2.resize(im, (new_width, new_height))

    # create Selective Search Segmentation Object using default parameters
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    # set input image on which we will run segmentation
    ss.setBaseImage(im)

    # Switch to fast but low recall Selective Search method
    if ss_type == 'f':
        ss.switchToSelectiveSearchFast()

    # Switch to high recall but slow Selective Search method
    elif ss_type == 'q':
        ss.switchToSelectiveSearchQuality()
    # if argument is neither f nor q print help message
    else:
        print(__doc__)
        sys.exit(1)

    # run selective search segmentation on input image
    rects = ss.process()
    print('Total Number of Region Proposals: {}'.format(len(rects)))

    # number of region proposals to show
    numShowRects = 100
    # increment to increase/decrease total number of reason proposals to be shown
    increment = 50

    ss_bbox = []
    while True:
        # create a copy of original image
        imOut = im.copy()
        ss_bbox.append(imOut)

        # itereate over all the region proposals
        for i, rect in enumerate(rects):
            # draw rectangle for region proposal till numShowRects
            if i < numShowRects:
                x, y, w, h = rect
                cv2.rectangle(imOut, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.LINE_AA)
            else:
                break

    return ss_bbox


if __name__ == '__main__':
    for bbox in selective_search(cv2.imread('/home/lucasx/Documents/talor.jpg')):
        cv2.imshow('img', bbox)
        cv2.waitKey(0)
