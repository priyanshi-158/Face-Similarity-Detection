## Model Documentation & Details

**Facial Similarity Detection System** is a technology capable of matching a human face from a digital image or a video frame against a database of faces, typically employed to authenticate users through ID verification services, works by pinpointing and measuring facial features from a given image.

We'll be building a face recognition model that uses **Siamese Networks** and takes 3 input images to give us a distance value that indicates which of these 2 images are similar or dissimilar to the anchor image.

#### **The Dataset**

We'll be using the **Extracted Faces** from **face-recognition-dataset**, which is derived from the **LFW Dataset**.
The Extracted Faces contains faces extracted from the base images using **Haar-Cascade Face-Detection** (CV2).

- The dataset contains 1324 different individuals, with 2-50 images per person.
- The images are of size (128,128,3) and are encoded in RGB.
- Each folder and image is named with a number, i.e 0.jpg, 1.jpg

#### How we built & trained the model.

- Load the dataset
- Preprocess the images
- Create triplets: We use the train and test list to create triplets of **(anchor, postive, negative)** face data, where positive is the same person and negative is a different person than anchor.
- Creating Batch-Generator: Creating a **Batch-Generator** that converts the triplets passed into batches of face-data and **preproccesses** it before returning the data into seperate lists.
- Plotting the data generated from **get_batch()** to see the results.
- Encoding: The **Encoder** is responsible for converting the passed images into their feature vectors.
- Creating a siamese network that takes 3 input images, (anchor, postive, negative) and uses the encoder above to encode the images to their feature vectors.
- These feature vectors are passed to a distance layer which computes the distance between **(anchor, positive)** and **(anchor, negative)** pairs.
- The model is trained using **Triplet Loss** which minimizes the distance between the anchor and positive images and maximizes the distance between the anchor and negative images.
- We trained the siamese_model on batches of triplets. The model weights were also saved whenever it outperforms the previous max_accuracy.

#### Using the model

Refer to the **Backend Documentation** for details on how to use the model API.
