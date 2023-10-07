from lexset.review import analysis

#dir_path = "C:/Users/franc/Downloads/landing_debug/Lexset SDK check/Lexset SDK check - dataset/88_real_board_image/"

dir_path = "C:/Users/franc/Downloads/landing_debug/Lexset SDK check/Lexset SDK check - dataset/09-08-lexset_new_synthetic_data/"

# Create an instance of the 'analysis' class
sample_data = analysis(dir_path)

#sample_data.plot_pixel_intensity_distribution()

#sample_data.plot_pixel_intensity_distribution("other")


#sample_data.spatial_analysis()
sample_data.relative_scale()
sample_data.bounding_box_areas()
sample_data.aspect_ratio_distribution()
#sample_data.plot_pixel_intensity_distribution()
#or 
#sample_data.plot_pixel_intensity_distribution("other")
sample_data.class_distribution()

# ##########################
# #(FID)
# #################################

# dir1 = "D:/LL_projects/medtronic/coco-dataset/09-08-lexset_new_synthetic_data/"
#dir2 = "C:/Users/franc/Downloads/landing_debug/Lexset SDK check/Lexset SDK check - dataset/09-08-lexset_new_synthetic_data/"
dir2 = "C:/Users/franc/Downloads/landing_debug/Lexset SDK check/Lexset SDK check - dataset/88_real_board_image/"
# # Create an instance of the 'analysis' class
# sample_data = analysis(dir1)
# #sample_data.calculate_FID(compare_dir=dir2)

# #######################################
# #Power Spectral Density:
# sample_data.plot_comparative_psd(compare_dir=dir2)
# #################################


#############################
#Structural Similarity Index (SSIM)
###################################
sample_data.compare_ssim_distributions(compare_dir=dir2,target_size=(2000, 2000))