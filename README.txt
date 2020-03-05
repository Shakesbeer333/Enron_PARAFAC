################################################### README ###################################################

# Configurations are set in the dev.ini document

# Download the Enorn email data set via https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz

# First,use script email_parser.py to parse the (raw) Enron email dataset. All relevent emails are stored in a pandas dataframe.

# Afterwards, use script term_weighting.py to translate the emails into bag-of-words, clean the data and subsequently store it in a three-dimensional (author x time x terms) tensor.

# Next, use script tensor_decomposition.py to apply non-negative PARAFAC on the three-dimensional tensor.

# Use script plot.py to plot the latent discussions' intensity over time

# Use script display.py to display the latent terms and authors of each discussion

###############################################################################################################

 

