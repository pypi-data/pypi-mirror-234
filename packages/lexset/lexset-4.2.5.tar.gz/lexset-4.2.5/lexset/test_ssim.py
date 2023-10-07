from review import analysis


dir1 = "D:/github/coco_analysis/5869/"
# dir2 = "D:/github/medtronic/real_img/"

# # Create an instance of the 'analysis' class
sample_data = analysis(dir1)
# #sample_data.compare_ssim_distributions(compare_dir=dir2,target_size=(256, 256))
# sample_data.calculate_FID(compare_dir=dir2)
sample_data.plot_pixel_intensity_distribution()

# from lexset.LexsetManager import merge_datasets

# # Define the directories containing your COCO JSON files and images
# json_dirs = ["D:/github/combine_coco_data/16744", "D:/github/combine_coco_data/16745"]

# # Define the percentage of data to keep from each directory
# percentages = [50, 50]  # 50% from the first directory, 60% from the second

# # Define paths to output JSON and image directory
# output_json_path = "D:/github/combine_coco_data/merge_test_3/coco_annotations.json"
# output_img_dir = "D:/github/combine_coco_data/merge_test_3/"

# # Merge the datasets
# merge_datasets(json_dirs, percentages, output_json_path, output_img_dir)