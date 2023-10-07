import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math
import matplotlib.gridspec as gridspec
from collections import Counter
import os
import os.path
import cv2
import re
from skimage.metrics import structural_similarity as ssim
import tensorflow as tf
from scipy.linalg import sqrtm
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

class analysis:

    #init
    def __init__(self,Dir):

        self.dir = Dir
        #validate dir is a string and ends with a slash
        if not isinstance(self.dir, str):
            raise TypeError("dir must be a string")
        if not self.dir.endswith("/"):
            raise ValueError("dir must end with a slash")

    # THIS FUNCTION WILL GENERATE A HEATMAP FOR EACH CATEGORY IN THE DATASET SHOWING THE DISTRIBUTION OF OBJECTS IN THE IMAGE FRAME.

    #performs spatial analysis on a dataset containing bounding box annotations of objects. 
    #The goal is to create heatmaps representing the distribution of object centers across 
    # different categories within the dataset.

    def spatial_analysis(self,num_bins=50):
        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a map from category_id to category_name and initialize storage for object centers
        id_to_category = {category["id"]: category["name"] for category in data["categories"]}
        object_centers = defaultdict(list)  # This will create a new list for a key if it doesn't exist

        # Compute the center of each bounding box
        for annotation in data["annotations"]:
            bbox = annotation['bbox']
            center = [(bbox[0] + bbox[2] / 2), (bbox[1] + bbox[3] / 2)]  # normalized x and y centers
            category = id_to_category[annotation["category_id"]]
            object_centers[category].append(center)

        # Compute the number of categories
        num_categories = len(object_centers)

        # Create a new figure with a subplot for each category
        fig = plt.figure(figsize=(10, num_categories*5))

        # Create a gridspec for layout control
        gs = gridspec.GridSpec(num_categories, 2, width_ratios=[20, 1])

        # Create a heat map for each category
        for i, (category, centers) in enumerate(object_centers.items()):
            heatmap, xedges, yedges = np.histogram2d(*zip(*centers), bins=num_bins)  # adjust bins for different resolution
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

            # Plot the heat map
            ax = plt.subplot(gs[i, 0])
            im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot')
            ax.set_title(category)

            # Add a colorbar for this heatmap in the second column of the grid
            cbax = plt.subplot(gs[i, 1])
            plt.colorbar(im, cax=cbax)

        plt.tight_layout()
        plt.savefig('heatmaps.png', bbox_inches='tight')  # Save the plot as a PNG file


        #analyzes a dataset containing object annotations and generates a bar plot 
        # representing the distribution of different classes (categories) present in the dataset. 

    def class_distribution(self):

        def get_class_distribution(json_file):
            # Load JSON data
            with open(json_file) as f:
                data = json.load(f)

            # Extract categories from the data
            id_to_category = {category["id"]: category["name"] for category in data["categories"]}

            # Count the occurrences of each category in the annotations
            counter = Counter(annotation["category_id"] for annotation in data["annotations"])

            # Convert category ids to names and count
            class_distribution = {id_to_category[id]: count for id, count in counter.items()}

            return class_distribution

        def plot_class_distribution(class_distribution, output_file):
            # Prepare data for plotting
            classes = list(class_distribution.keys())
            counts = list(class_distribution.values())

            # Create bar plot
            plt.figure(figsize=(10, 6))
            plt.barh(classes, counts, color='skyblue')
            plt.xlabel("Count")
            plt.ylabel("Classes")
            plt.title("Class Distribution")
            plt.tight_layout()

            # Save the plot as a PNG file
            plt.savefig(output_file)

        json_file = self.dir + "coco_annotations.json"
        output_file = "class_distribution.png"

        distribution = get_class_distribution(json_file)
        plot_class_distribution(distribution, output_file)


    #performs relative size analysis on a dataset containing object annotations 
    # with bounding box information. The goal is to analyze the relative size 
    # of objects within each category and visualize the distribution of relative 
    # sizes using histograms.

    def relative_scale(self, num_bins=50):

        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a dictionary to hold relative sizes per category
        relative_sizes = {category['id']: [] for category in data['categories']}

        # Iterate over annotations
        for annotation in data['annotations']:
            # Get bounding box dimensions
            box_width = annotation['bbox'][2]
            box_height = annotation['bbox'][3]

            # Get image dimensions
            for image in data['images']:
                if image['id'] == annotation['image_id']:
                    img_width = image['width']
                    img_height = image['height']
                    break

            # Compute relative size and add it to the list
            relative_sizes[annotation['category_id']].append((box_width * box_height) / (img_width * img_height))

        # Compute the layout for the subplots (as a square grid, or as close to a square as possible)
        num_categories = len(data['categories'])
        grid_size = math.ceil(math.sqrt(num_categories))

        # Check if there will be multiple subplots
        if num_categories > 1:
            fig, axs = plt.subplots(grid_size, grid_size, figsize=(15, 15))
            axs = axs.flat  # Flatten the array for easy indexing
        else:
            fig, ax = plt.subplots(figsize=(15, 15))
            axs = [ax]  # Create a list with the single axis for consistent indexing

        # Plot a histogram of relative sizes for each category
        for i, category in enumerate(data['categories']):
            ax = axs[i]
            ax.hist(relative_sizes[category['id']], bins=num_bins)
            ax.set_title(category["name"])

        # Remove any unused subplots
        if num_categories < grid_size * grid_size:
            for j in range(num_categories, grid_size * grid_size):
                fig.delaxes(axs[j])

        plt.tight_layout()
        plt.savefig('relative_sizes.png', bbox_inches='tight')  # Save the plot as a PNG file

    #analyzes a dataset containing object annotations with bounding box information. 
    # The goal is to compute the areas of bounding boxes for each object category and 
    # visualize the distribution of these areas using histograms.

    def bounding_box_areas(self, num_bins=50):
            
        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a map from category_id to category_name and initialize storage for bbox areas
        id_to_category = {category["id"]: category["name"] for category in data["categories"]}
        bbox_areas = defaultdict(list)  # This will create a new list for a key if it doesn't exist

        # Compute bounding box areas
        for annotation in data["annotations"]:
            bbox = annotation['bbox']
            bbox_area = bbox[2] * bbox[3]  # width * height
            category = id_to_category[annotation["category_id"]]
            bbox_areas[category].append(bbox_area)

        # Create histogram
        num_categories = len(bbox_areas)

        # Check for single category
        if num_categories == 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            axs = [ax]  # Make it a list to be consistent with the multiple categories case
        else:
            fig, axs = plt.subplots(num_categories, 1, figsize=(10, 6 * num_categories))

        # Create histogram for each category
        for (category, areas), ax in zip(bbox_areas.items(), axs):
            if areas:  # Check if areas list is not empty
                ax.hist(areas, bins=np.linspace(0, max(areas), num_bins), color='blue', alpha=0.5)
                ax.set_title(category)
                ax.set_xlabel("Area")
                ax.set_ylabel("Frequency")

        fig.tight_layout()  # Adjusts subplot params so that subplots are nicely fit in the figure area
        plt.savefig('bbox_areas.png', bbox_inches='tight')  # Save the plot as a PNG file

    #performs aspect ratio analysis on a dataset containing object annotations with bounding box information. 
    # The goal is to calculate the aspect ratio of bounding boxes for each object category and visualize 
    # the distribution of these aspect ratios using histograms.

    def aspect_ratio_distribution(self, num_bins=50):
            
        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a map from category_id to category_name and initialize storage for annotations
        id_to_category = {category["id"]: category["name"] for category in data["categories"]}
        annotations = defaultdict(list)

        # Group annotations by category
        for annotation in data["annotations"]:
            category = id_to_category[annotation["category_id"]]
            annotations[category].append(annotation)

        # Create a subplot for each category
        num_categories = len(annotations)

        # Check for single category
        if num_categories == 1:
            fig, ax = plt.subplots(figsize=(10, 5))
            axs = [ax]  # Make it a list to be consistent with the multiple categories case
        else:
            fig, axs = plt.subplots(num_categories, 1, figsize=(10, num_categories*5))

        for ax, (category, category_annotations) in zip(axs, annotations.items()):
            # Prepare storage for aspect ratios
            aspect_ratios = []

            # Calculate aspect ratio for each bounding box
            for annotation in category_annotations:
                bbox = annotation['bbox']
                # Check for zero width or height to avoid division by zero
                if bbox[2] > 0 and bbox[3] > 0:
                    aspect_ratio = bbox[2] / bbox[3]  # assuming bbox format is [xmin, ymin, width, height]
                    aspect_ratios.append(aspect_ratio)

            # Create a histogram of the aspect ratios
            ax.hist(aspect_ratios, bins=num_bins)
            ax.set_title(f'Distribution of Aspect Ratios for {category}')
            ax.set_xlabel('Aspect Ratio (width/height)')
            ax.set_ylabel('Frequency')

        plt.tight_layout()
        plt.savefig('aspect_ratio_distribution.png')



    def plot_pixel_intensity_distribution(self, type = "Lexset"):
        all_images = os.listdir(self.dir)
        channels = ['Red', 'Green', 'Blue']
                                
        # Create a regex pattern to match any of the valid image extensions
        valid_ext_pattern = r"\.(jpg|png|tiff|tif|bmp)$"

        # Combine it with the rest of your original pattern
        full_pattern = r"\.rgb_\d{4}" + valid_ext_pattern
        
        # Initialize valid_images to an empty list
        valid_images = []

        if type == "Lexset":
            valid_images = [img for img in all_images if re.search(full_pattern, img)]

            # Populate valid_images with matched filenames
            valid_images = [img for img in all_images if re.search(full_pattern, img)]
        else:
            valid_images = [img for img in all_images if os.path.splitext(img)[1].lower() in ['.jpg', '.png', '.tiff', '.tif', '.bmp']]

        def calculate_pixel_histogram(image_path, channel):
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            channel_values = img[:, :, channel].flatten()
            hist, _ = np.histogram(channel_values, bins=256, range=[0, 256])
            return hist / np.sum(hist)
        
        channel_colors = {'Red': (1, 0, 0), 'Green': (0, 1, 0), 'Blue': (0, 0, 1)}

        for channel in range(3):
            aggregated_hist = np.zeros(256)
            for image in valid_images:
                image_path = os.path.join(self.dir, image)
                image_hist = calculate_pixel_histogram(image_path, channel)
                aggregated_hist += image_hist

            aggregated_hist /= len(valid_images)
            plt.plot(aggregated_hist, label=channels[channel], color=channel_colors[channels[channel]])

        plt.title("pixel_intensity_distribution")
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Normalized Frequency')
        plt.legend()

        # Save plot instead of showing it
        plt.savefig("pixel_intensity_distribution.png")


    def calculate_average_psd(self, image_dir, target_size=(256, 256)):
        images = os.listdir(image_dir)
        total_psd = None
        count = 0

        naming_convention_exists = any(re.search(r'\.rgb_\d{4}\.png$', img) for img in images)
        #print("Naming convention exists: ", naming_convention_exists)

        if naming_convention_exists:
            # Use only images that follow the naming convention
            valid_images = [img for img in images if re.search(r'\.rgb_\d{4}\.(jpg|png|tiff|tif|bmp)$', img, re.IGNORECASE)]
        else:
            # Use all images with valid extensions
            valid_images = [img for img in images if os.path.splitext(img)[1].lower() in ['.jpg', '.png', '.tiff', '.tif', '.bmp']]
        
        #print(valid_images)

        for img_name in valid_images:
            #print(img_name)
            img_path = os.path.join(image_dir, img_name)
            if img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp')):
                img = cv2.imread(img_path, 0)  # read as grayscale
                img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
                if total_psd is None:
                    total_psd = np.zeros_like(img, dtype=float)
                f_transform = np.fft.fft2(img)
                f_transform_shifted = np.fft.fftshift(f_transform)
                psd = np.abs(f_transform_shifted) ** 2
                total_psd += psd
                count += 1
        if count == 0:
            print("No valid images found in directory.")
            return None
        average_psd = total_psd / count
        return average_psd

    def plot_comparative_psd(self, compare_dir):
        avg_psd1 = self.calculate_average_psd(self.dir)
        avg_psd2 = self.calculate_average_psd(compare_dir)
        
        plt.figure()
        
        plt.subplot(1, 2, 1)
        plt.imshow(np.log1p(avg_psd1), cmap='gray')
        plt.title('Synthetic Data')
        
        plt.subplot(1, 2, 2)
        plt.imshow(np.log1p(avg_psd2), cmap='gray')
        plt.title(f'Comparison Data')
        
        plt.savefig('average_psd_comparison.png')  # Save the figure
        plt.close()  # Close the figure to free up memory
        
        # Compute the difference between the two average PSDs
        difference_map = np.abs(avg_psd1 - avg_psd2)

        # Plot and save the difference map
        plt.figure()
        plt.imshow(np.log1p(difference_map), cmap='hot')
        plt.title(f'Difference between PSDs')
        plt.colorbar()
        plt.savefig('difference_psd.png')  # Save the figure
        plt.close()  # Close the figure to free up memory
        
        # Compute the ratio between the two average PSDs, avoid division by zero
        ratio_map = avg_psd1 / (avg_psd2 + 1e-8)

        # Plot and save the ratio map
        plt.figure()
        plt.imshow(ratio_map, cmap='coolwarm', vmin=0, vmax=2)
        plt.title(f'Ratio between PSDs')
        plt.colorbar()
        plt.savefig('ratio_psd.png')  # Save the figure
        plt.close()  # Close the figure to free up memory


    def calculate_ssim_for_images(self, image_path1, image_path2, target_size=(256, 256)):
        img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

        if img1 is None:
            raise FileNotFoundError(f"File not found or couldn't be read: {image_path1}")
        if img2 is None:
            raise FileNotFoundError(f"File not found or couldn't be read: {image_path2}")

        img1 = cv2.resize(img1, target_size, interpolation=cv2.INTER_LINEAR)
        img2 = cv2.resize(img2, target_size, interpolation=cv2.INTER_LINEAR)

        return ssim(img1, img2)

    def compare_ssim_distributions(self, compare_dir, target_size=(256, 256)):
        synthetic_images = os.listdir(self.dir)
        real_images = os.listdir(compare_dir)

        # Filter out only valid synthetic images
        naming_convention_exists = any(re.search(r'\.rgb_\d{4}\.(jpg|png|tiff|tif|bmp)$', img, re.IGNORECASE) for img in synthetic_images)
        if naming_convention_exists:
            valid_synthetic_images = [img for img in synthetic_images if re.search(r'\.rgb_\d{4}\.(jpg|png|tiff|tif|bmp)$', img, re.IGNORECASE)]
        else:
            valid_synthetic_images = [img for img in synthetic_images if os.path.splitext(img)[1].lower() in ['.jpg', '.png', '.tiff', '.tif', '.bmp']]

        # Filter out only valid real images
        valid_real_images = [img for img in real_images if os.path.splitext(img)[1].lower() in ['.jpg', '.png', '.tiff', '.tif', '.bmp']]

        synthetic_ssim_values = []

        for synthetic_image in valid_synthetic_images:
            synthetic_image_path = os.path.join(self.dir, synthetic_image)
            real_image_path = os.path.join(compare_dir, valid_real_images[np.random.randint(len(valid_real_images))])

            ssim_value = self.calculate_ssim_for_images(synthetic_image_path, real_image_path, target_size)
            synthetic_ssim_values.append(ssim_value)

        mean_ssim = np.mean(synthetic_ssim_values)
        print(f"Mean SSIM between synthetic and real images: {mean_ssim}")

        with open("ssim_results.json", "w") as json_file:
            json.dump({'mean_ssim': mean_ssim, 'individual_ssim': synthetic_ssim_values}, json_file)

    def calculate_FID(self, compare_dir):
        # Function to preprocess the image
        def preprocess_image(image_path, target_size=(299, 299)):
            image = cv2.imread(image_path)
            image = cv2.resize(image, target_size)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return np.expand_dims(image, axis=0)

        # Helper function to check if a file is an image and optionally matches a naming convention
        def is_image_file(filename, naming_convention=False):
            if naming_convention:
                return re.search(r'\.rgb_\d{4}\.(jpg|png|tiff|tif|bmp)$', filename, re.IGNORECASE) is not None
            else:
                return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.tif'))

        # Detect if naming convention exists in any of the images in self.dir
        naming_convention_exists = any(re.search(r'\.rgb_\d{4}\.png$', img) for img in os.listdir(self.dir))

        # Create lists of valid image paths
        reference_image_paths = [os.path.join(compare_dir, fname) for fname in os.listdir(compare_dir) if is_image_file(fname)]

        if naming_convention_exists:
            synthetic_data_paths = [os.path.join(self.dir, fname) for fname in os.listdir(self.dir) if is_image_file(fname, naming_convention=True)]
        else:
            synthetic_data_paths = [os.path.join(self.dir, fname) for fname in os.listdir(self.dir) if is_image_file(fname)]

        # Load and preprocess images
        reference_images = np.vstack([preprocess_image(path) for path in reference_image_paths])
        synthetic_data_images = np.vstack([preprocess_image(path) for path in synthetic_data_paths])

        # Load the InceptionV3 model
        inception_model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet', input_shape=(299, 299, 3), pooling='avg')

        # Compute activations for reference and synthetic data images
        reference_activations = inception_model.predict(reference_images)
        synthetic_data_activations = inception_model.predict(synthetic_data_images)

        # Compute the mean and covariance for the reference and synthetic data activations
        reference_mean = np.mean(reference_activations, axis=0)
        synthetic_data_mean = np.mean(synthetic_data_activations, axis=0)

        reference_covariance = np.cov(reference_activations, rowvar=False)
        synthetic_data_covariance = np.cov(synthetic_data_activations, rowvar=False)

        # Compute the squared Euclidean distance between the means
        squared_distance = np.sum((reference_mean - synthetic_data_mean) ** 2)

        # Compute the trace of the product of the covariance matrices
        covmean = sqrtm(reference_covariance.dot(synthetic_data_covariance))
        if np.iscomplexobj(covmean):
            covmean = covmean.real
        trace_product = np.trace(reference_covariance + synthetic_data_covariance - 2.0 * covmean)

        # Compute the FID
        fid_value = squared_distance + trace_product

        # Print the FID
        print(f'Fréchet Inception Distance between the sets of images: {fid_value:.2f}')

        with open('FID_Score.json', 'w') as json_file:
            json.dump({"FID": fid_value}, json_file)

        # Combine both sets of activations for PCA
        all_activations = np.vstack([reference_activations, synthetic_data_activations])
        pca = PCA(n_components=2)
        reduced_activations = pca.fit_transform(all_activations)

        # Plot
        plt.scatter(reduced_activations[:len(reference_activations), 0], reduced_activations[:len(reference_activations), 1], label='Reference')
        plt.scatter(reduced_activations[len(reference_activations):, 0], reduced_activations[len(reference_activations):, 1], label='Synthetic Data')
        plt.legend()
        plt.title('PCA Reduced Activations')
        #plt.show()
        plt.savefig('FID_PCA_Reduced_Activations.png')  # Save the plot as a PNG file

