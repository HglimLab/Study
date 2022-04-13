## Object Detection이란?

- 영상 내에 존재하는 모든 카테고리에 대해서 classification(분류)과 localization(지역화)를 수행하는 task
  - Localization은 bounding box를 찾는 regression(회귀)이고, classification은 bounding box 내 물체가 무엇인지 분류하는 문제

### Object detection vs semantic segmentation

- semantic segmentation은 각 픽셀에 대해 클래스를 정해주는 문제

![image](https://user-images.githubusercontent.com/102014209/163134382-e8def046-71ff-484f-95a0-3cb9ed15c011.png)

### Measurement(평가)
- IoU(Intersection over Unit)
  - Object detection에서 bounding box를 얼마나 잘 예측하였는지는 IoU라는 지표를 통해 측정. 정답인 GT(Ground Truth)와 예측된 bounding box가 얼마나 겹치는가를 측정
- Confusion matrix(혼동행렬)

![image](https://user-images.githubusercontent.com/102014209/163135915-2d04eefa-1671-4328-b847-4f97e020bb53.png)

- Recall
  - 재현율, 검출 돼야하는 물체들 중 제대로 검출된 비율
  - TP/(TP + FN)

- Precision
  - 정밀도, 옳게 검출한 비율, Recall과 반비례 관계
  - TP/(TP + FP)
