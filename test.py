from radiomics import featureextractor
import SimpleITK as sitk

image_path = r"C:\Users\klaud\OneDrive\Desktop\stopa.jpg"
mask_path = r"C:\Users\klaud\OneDrive\Desktop\maska_stopy.jpg"

image = sitk.ReadImage(image_path, sitk.sitkUInt8)
mask = sitk.ReadImage(mask_path, sitk.sitkUInt8)

image.SetSpacing((1.0, 1.0))
mask.SetSpacing((1.0, 1.0))

mask = sitk.BinaryThreshold(mask,
                             lowerThreshold=1,
                             upperThreshold=255,
                             insideValue=1,
                             outsideValue=0)

mask.CopyInformation(image)

extractor = featureextractor.RadiomicsFeatureExtractor()

extractor.disableAllFeatures()
#extractor.enableFeaturesByName(glcm=['JointAverage'])
extractor.enableFeatureClassByName("glcm")

result = extractor.execute(image, mask)

for key, value in result.items():
    if 'glcm' in key.lower():
        print(f"{key}: {value}")