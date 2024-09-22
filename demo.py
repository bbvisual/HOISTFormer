import os
import os.path as osp
import cv2
import numpy as np
import argparse
from demo_video.predictor import VisualizationDemo

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Arguments for Demo')
    parser.add_argument('--video_frames_path', required=True, metavar='path to images', help='path to images')
    args = parser.parse_args()

    weights_path = './pretrained_models/trained_model.pth'
    cfg_file = './configs/hoist/hoistformer.yaml'
    demo_inference = VisualizationDemo(cfg_file, weights_path)

    root = args.video_frames_path
    output_path = './output_results/'
    videos = os.listdir(root)
    for vid_idx, vid in enumerate(videos):
        print(f'Processing video: {vid_idx}, total: {len(videos)}')
        frames_bgr_np = []
        frames = sorted(os.listdir(osp.join(root, vid)))
        for frm in frames:
            frm_np = cv2.imread(osp.join(root, vid, frm))
            frames_bgr_np.append(frm_np)
        predictions, vis_output = demo_inference.run_on_video(frames_bgr_np)
        os.makedirs(osp.join(output_path, vid), exist_ok=True)
        for frm_idx, vis_img in enumerate(vis_output):
            frm = vis_img.get_image()
            save_path = osp.join(output_path, vid, f'output_frm_{frm_idx}.jpg')
            cv2.imwrite(save_path, frm)