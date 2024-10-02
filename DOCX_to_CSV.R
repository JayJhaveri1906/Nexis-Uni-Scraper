# Install and load necessary package
install.packages("LexisNexisTools")
library("LexisNexisTools")

# Define the path to the main Downloads directory
main_dir <- "./Downloads"

# Get a list of all subdirectories within the main directory
subfolders <- list.dirs(main_dir, recursive = FALSE)

# Loop through each subfolder
for (subfolder in subfolders) {
  # Find the DOCX file in each subfolder (assuming one DOCX file per folder)
  docx_files <- list.files(subfolder, pattern = "\\.DOCX$", full.names = TRUE)
  
  if (length(docx_files) > 0) {
    # Process the DOCX file (assuming only one DOCX file per subfolder)
    docx_file <- docx_files[1]  # Take the first DOCX file if multiple are found
    
    # Read the LexisNexis document
    LNToutput <- lnt_read(x = docx_file)
    
    # Extract the metadata, articles, and paragraphs
    meta_df <- LNToutput@meta
    articles_df <- LNToutput@articles
    paragraphs_df <- LNToutput@paragraphs
    
    # Print subfolder name and dimensions of the articles dataframe
    print(subfolder)
    print(dim(articles_df))
    
    # Convert the metadata and articles into a data frame
    meta_articles_df <- lnt_convert(LNToutput, to = "data.frame")
    
    # Define output CSV file name based on the subfolder name
    subfolder_name <- basename(subfolder)
    output_csv <- paste0(subfolder_name, "_meta_articles.csv")
    
    # Write the data to a CSV file
    write.csv(meta_articles_df, file = file.path(subfolder, output_csv), row.names = FALSE)
  } else {
    # If no DOCX file is found in the subfolder, print a message
    print(paste("No DOCX file found in", subfolder))
  }
}
