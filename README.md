# PARAFAC decomposition on the Enron E-Mail data set

Disclaimer: For the original idea of this project see
[Bader B.W., Berry M.W., Browne M. (2008) Discussion Tracking in Enron Email Using PARAFAC. In: Berry M.W., Castellanos M. (eds) Survey of Text Mining II. Springer, London.](https://doi.org/10.1007/978-1-84800-046-9_8)

## Scientific background

Texts present an alternative perspective on a subject of interest (Acosta (2015)).  Unlike quantitative data, i.e.  numbers, texts are generally edited by a human which makesqualitative data diverse (Acosta (2015)).  Each document is individual as both styleand content of the document convey the author’s mindset (Acosta (2015)).  On the contrary, numbers communicate an objective perception.  Moreover, some information isonly available in a qualitative format. For instance, a time series of email conversationsmight reflect a decision making process of an institution, whereas numbers fail to doso (Acosta (2015)).  In some cases, qualitative data contain more valuable informationthan  structured  data.   According  to  Kloptchenko  et  al.  (2004),  ”the  textual  part  of an annual [company] report contains richer information than financial ratios.” Hence,qualitative data can provide new insights into the functioning of complex structuressuch as companies or social networks (Acosta (2015)).

The issue that comes along with unstructured data is the large amount of data.  Key performance indicators can usually be expressed with two numbers, whereas it takes several words to describe the performance of a company.  In order to facilitate interpretation of textual data, it is essential to reduce these large data volumes to a manageable size (Bader et al. (2007)).  Whenever a type of relationship can be expressed as a (high-dimensional) matrix,  e.g.  term frequencies in documents,  performing decomposition allows to detect latent structures in the underlying data (Rabanser et al. (2017)).  The challenge is to determine thetrue  influencing  factorsthat account for the empiricaldata relationships (Harshman (1970)).

The extent to which standard data analysis methods such as Singular Value Decomposition (SVD) offer explanatory power has always been controversial (Harshman (1970)). If a two-dimensional representation of data shares more than one latent variable, the seclassical models tolerate multiple sets of influencing factors (Harshman (1970); Acaret al. (2005)). All possible factor combinations are mathematically equivalent withinthe model (Harshman (1970)).  However, all valid solutions result in a different interpretation of the explanatory variables of the underlying data relationships (Harshman(1970)).  Literature states this issue asrotation  problem (Bro (1997)).  On the otherhand,  one  could  ask  why  this  is  a  problem  in  real  applications. It is  certainly  rea-sonable to argue, that any complex system can be defined in several ways (Harshman(1970)).  Harshman (1970) points out that ”explanatory descriptions have implications beyond  the  current  set  of  measurements  being  described. Explanatory descriptions imply predictions about the results of other possible experiments.” Thus, explanatoryvariables which equally well fit a particular set of observations are most likely not thetrue influencing factorsof the population (Harshman (1970)). 

Research in numerous areas, including neuroscience, process analysis, social networksand text-mining confirm that two-dimensional data analysis techniques do not accurately  capture  the  latent  profiles  of  the  data  i.e. uniquelyidentify  the  underlying information content (Acar and Yener (2009)).  For example, Acar et al. (2005) demon-strate that SVD cannot completely detect the multilinear structure which is present inchatroom communication data as it might be noisy and multidimensional.  The problem does not arise from the data decomposition techniques themselves but rather fromthe low dimension of the data onto which the two-way analysis methods are applied. Acar and Yener (2009) argue that ”matrices are often not enough to represent all theinformation content of the data.” By contrast,  multiway data analysis tools like the  Parallel Factor (PARAFAC) method enable to discover the latent structure in higher-dimensional data - with the advantage of robustness to noise andunique decomposition(Acar and Yener (2009)). Literature refers to these multidimensional data structures as tensors(Rabanser et al. (2017)).

In this work,  I apply the PARAFAC decomposition on the publicly released Enron email dataset.  The objective is to uncover meaningful discussion threads in the email network  over  time.   To  the  best  of  my  knowledge,  Bader  et  al.  (2008)  are  the  firstwho apply a generalization of SDV on an email corpus, namley the email conversations within Enron (Acar et al. (2005)).  My work replicates Bader et al. (2008)’s procedureto get a better understanding of extracting latent structures in a set of unstructured documents i.e.  emails (Bader et al. (2008)). I approach the PARAFAC decomposition as follows.  First, I filter for emails written in  2001  which  is  the  year  when  Enron  filed  for  bankruptcy  (Bader  et  al.  (2008)). Moreover, I only consider email addresses which have been identified by Priebe et al.(2015) as worthwhile to investigate in.  Next, I break down the body of the email intoweighted word frequencies.  I omit certain terms to focus on the meaningful context.From the remaining content,  I create a data-cube with thethree  dimensions  author,time  and term allowing for aunique decompositionin the subsequent step.  Applying the PARAFAC tool provided by Kossaifi et al. (2019) on this three-dimensional tensor decomposes  the  email  corpus  of  Enron  into  14  threads  of  discussion.   The  ten  mostdominant words of each conversation, i.e.  words having the largest weighting, can thenbe  used  to  define  a  topic  for  the  corresponding  discussion.   Additionally,  the  result allows to track the discussions’ intensity over time.

I identify two of 14 conversation topics as meaningful, namely Law & Regulation and California.  For instance, the dominant term mismanagement can be connected to the California energy crisis of 2000 and 2001 during which Enron generated huge profit (Eichenwald and Richtel (2002)).  The latent word Monterey links to California as it is a city of this state. Montereyseems to be a gateway for Enron’s interests in California.Of the remaining twelve conversations only particular latent terms such as gasoline link to activities that Enron had been involved in.  These poor results might be due to noise in the data.  Further investigation reveal for example that single emails are written in polish  as  the  latent  term serdeczn suggests.   In  comparison,  Bader  et  al.  (2008)  identify eight of 25 discussions as expressive.  From these observations I conclude the following.  First, preprocessing the data is a crucial step for decomposing unstructured documents.  The human-generated stopword list of Bader et al. (2008) contains more than 47k words,  whereas mine consists of approximately 200 stopwords provided bythe  Natural  Language  Toolkit  (NLTK)  and  17  Regular  Expressions  (RegEx)  (Birdet  al.  (2017)).   This  difference  in  the  size  of  the  stopword  list  could  be  a  reason  for the  noise  in  my  data  and  consequently  the  poor  results  in  comparison  with  Baderet al. (2008).  Second, human intelligence is still necessary to interpret the connections between  dominant  terms  and  an  overarching  topic.   With  regards  to  preprocessing, human knowledge is also essential in identifying ”words with no specific reference toan Enron-related person or activity” in order to set up a stopword list (Bader et al.(2008)).

## How to use this repository

1) Configurations are set in the dev.ini document

2) Download the Enorn email data set via https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz

3) First, use script email_parser.py to parse the (raw) Enron email dataset. All relevent emails are stored in a pandas dataframe.

4) Afterwards, use script term_weighting.py to translate the emails into bag-of-words, clean the data and subsequently store it in a three-dimensional (author x time x terms) tensor.

5) Next, use script tensor_decomposition.py to apply non-negative PARAFAC on the three-dimensional tensor.

6) Use script plot.py to plot the latent discussions' intensity over time

7) Use script display.py to display the latent terms and authors of each discussion

## References

Acar, E., and B. Yener, 2009, Unsupervised multiway data analysis: A literature survey, IEEE Transactions on Knowledge and Data Engineering 21, 6–20.

Acar, Evrim, Seyit A. Camtepe, Mukkai S. Krishnamoorthy, and B ̈ulent Yener, 2005, Modeling  and  multiway  analysis  of  chatroom  tensors,  in Intelligence  and  Security Informatics, 256–268 (Springer Berlin Heidelberg).

Acosta,  Miguel,  2015,  FOMC  responses  to  calls  for  transparency,Finance  and  Economics Discussion Series 2015, 1–44.

Bader, B. W., R. A. Harshman, and T. G. Kolda, 2007, Temporal analysis of semantic graphs  using  asalsan,  in Seventh  IEEE  International  Conference  on  Data  Mining(ICDM 2007), 33–42.

Bader, Brett W., Michael W. Berry, and Murray Browne, 2008, Discussion tracking inenron email using PARAFAC (Michael W. Berry and Malu Castellanos).

Bashiri,   Mohammad,   2019,   Tensor  decomposition  in  python, https://medium.com/@mohammadbashiri93/tensor-decomposition-in-python-f1aa2f9adbf4 (accessed 20/11/2019).

Battaglino, Casey, Grey Ballard, and Tamara G. Kolda, 2018, A practical randomized CP tensor decomposition, SIAM  Journal  on  Matrix  Analysis  and  Applications 39, 876–901.

Berry, Michael W., and Murray Browne, 2005, Email surveillance using non-negativematrix factorization,Computational & Mathematical Organization Theory 11, 249–264.

Bhaskara, Aditya, Moses Charikar, and Aravindan Vijayaraghavan, 2014, Uniquenessof tensor decompositions with applications to polynomial identifiability, in Maria Florina Balcan, Vitaly Feldman, and Csaba Szepesv ́ari, eds.,Proceedings  of  The  27th Conference on Learning Theory, volume 35 of Proceedings of Machine Learning Research, 742–778 (PMLR, Barcelona, Spain).

Bird, Steven, Ewan Klein, and Edward Loper, 2017,Natural Language Processing with Python (O’Reilly Media)

Bro, Rasmus, 1997, Parafac. tutorial and applications, Chemometrics  and  IntelligentLaboratory Systems 38, 149–171.

Cohen,  William W.,  2015,  Enron email dataset, https://www.cs.cmu.edu/~enron/ (accessed 27/12/2019).

Eichenwald, Kurt, and Matt Richtel, 2002, Enron trader pleads guilty to conspiracy, The New York Times.

Hansen, Stephen, 2019, Text mining for economics and finance:  Introduction,https://sekhansen.github.io/pdf_files/lecture1.pdf (accessed 02/01/2020).

Hardin, Johanna, Ghassan Sarkis, and P. Urc, 2014, Network analysis with the enronemail corpus, Journal of Statistics Education 23.

Harshman, Richard A., 1970, Foundations of the parafac procedure:  Models and con-ditions for an ”explanatory” multi-model factor analysis, UCLA  working  papers  in phonetics 1–84.

Heidenreich,    Hunter,    2018,    Stemming?lemmatization?what?, https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8 (accessed 02/01/2020).

Kiers, Henk A.L., 1991, Hierarchical relations among three-way methods, Psychometrika 56, 449–470. 

Kloptchenko,  Antonina,  Tomas  Eklund,  Jonas  Karlsson,  Barbro  Back,  Hannu  Van-haranta,  and  Ari  Visa,  2004,  Combining  data  and  text  mining  techniques  for analysing  financial  reports,Intelligent  Systems  in  Accounting,  Finance  and  Management 12, 29–41.

Kolda, Tamara G., and Brett W. Bader, 2009, Tensor decompositions and applications, SIAM Review51, 455–500. Kossaifi, Jean, Yannis Panagakis, Anima Anandkumar, and Maja Pantic, 2019, Tensorly:  Tensor learning in python, Journal of Machine Learning Research 20, 1–6.

Kruskal, Joseph B., 1977, Three-way arrays:  rank and uniqueness of trilinear decom-positions,  with application to arithmetic complexity and statistics, Linear  Algebraand its Applications 18, 95 – 138.

Laub, Alan J., 2004, Matrix Analysis For Scientists And Engineers(Society for Industrial and Applied Mathematics, Philadelphia, PA, USA).

Manning, Christopher D., Prabhakar Raghavan, and Hinrich Sch ̈utze, 2008, Introduction to Information Retrieval (Cambridge University Press, USA).

Metzger, Julian, 2019, News implied volatility,Project Thesis at KIT.

Nitsuwat,  Supot,  2018,  Multilinear  principal  component  analysis  for  tensor  data:  A survey,Information Technology Journal 14, 38–47.

Priebe, Carey E., John M. Conroy, David J. Marchette, and Youngser Park, 2015, Scan statistics on enron graphs, http://cis.jhu.edu/~parky/Enron/enron.html.

Rabanser, Stephan, Oleksandr Shchur, and Stephan G ̈unnemann, 2017, Introduction to tensor decompositions and their applications in machine learning,https://arxiv.org/pdf/1711.10781.pdf (accessed 20/11/2019).

Sidiropoulos, Nicholas D., Lieven De Lathauwer, Xiao Fu, Kejun Huang, Evangelos E.Papalexakis, and Christos Faloutsos, 2017, Tensor decomposition for signal processing and machine learning, IEEE Transactions on Signal Processing 65, 3551–3582.

Sparse developers, 2018, Sparse,https://sparse.pydata.org/en/latest/ (accessed02/01/2020).

Stanimirova,  I.,  B.  Walczak,  D.L.  Massart,  V.  Simeonov,  C.A.  Saby,  and  E.  DiCrescenzo,  2004,  Statis,  a  three-way  method  for  data  analysis.  application  to  en vironmental data,Chemometrics and Intelligent Laboratory Systems 73, 219 – 233.

Tan,   Liling,   2017,   Basic   nlp   with   nltk,https://www.kaggle.com/alvations/basic-nlp-with-nltk#Stemming-and-Lemmatization (accessed 27/12/2019).

Weiss, Sholom M., Nitin Indurkhya, and Tong Zhang, 2010, Fundamentals of Predictive Text Mining, volume 41 of Texts in Computer Science(Springer).

Zhang, Huamin, and Feng Ding, 2013, On the kronecker products and their applications,Journal of Applied Mathematics2013, 1–8.

