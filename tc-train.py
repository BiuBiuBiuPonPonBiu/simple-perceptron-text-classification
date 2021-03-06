# Import standard modules
import sys
import pickle
from DataPrepper import DataPrepper
from PerceptronClassifier import PerceptronClassifier

#===========================================================================#
# TRAINING THE TEXT CLASSIFIER
# Executes the training phase of the text classifier on documents given in
# train-class-list. Saves the trained perceptron weights into the file
# called 'model'.
#
# Run with command:
#   python3 tc-train.py stopword-list train-class-list model
#===========================================================================#
class TextClassifier():
  def __init__(self):
    print("[TextClassifier] instantiated!")
    self.DataPrepper = DataPrepper(PATH_TO_STOP_WORDS, PATH_TO_TRAIN_CLASS_LIST)
    self.PerceptronClassifier = PerceptronClassifier()

  def build(self):
    print("[TextClassifier] Prepping dataset...")

    # Get all class names to make a perceptron classifier for
    class_names = self.DataPrepper.class_names

    # Initialize data structure to save doc freq and weights
    weight_docfreq_map = {}

    # Setup feature vectors for corpus
    feature_vectors_classes_docfreq = self.DataPrepper.run()
    feature_vectors_classes = feature_vectors_classes_docfreq[0]
    self.insert_bias(feature_vectors_classes)
    print('Dim of feature vector:', len(feature_vectors_classes[0][0]))
    doc_freq_map = feature_vectors_classes_docfreq[1]

    # For all classes in class_names, train a perceptron
    for class_name in class_names:
      f_train_vectors = self.setup_feature_vectors(class_name, feature_vectors_classes)
      X = f_train_vectors[0]
      y = f_train_vectors[1]
      w = self.PerceptronClassifier.train(X, y, learning_rate=0.02, num_epochs=15)
      weight_docfreq_map[class_name] = w
      print('=== FINISHED TRAINING MODEL FOR CLASS %s ===\n\n' % class_name)

    self.save_models([weight_docfreq_map, doc_freq_map])

  def save_models(self, models_df):
    print("[TextClassifier] Saving model to disk...")
    pickle.dump(models_df, open(PATH_TO_MODEL, 'wb'))

  def insert_bias(self, f_vectors_classnames):
    for f_vector_classname in f_vectors_classnames:
      f_vector_classname[0].insert(0, 1.0)

  """
  Sets feature_vectors into the correct shape, with its true y classification
  appended to the back of the feature vector's list

  Returns a tuple of X and y,
    where X is of the format with length n_samples:
    [[feature_vector_of_doc_1], [feature_vector_of_doc_2]...]

    where y is of the format with length n_samples, representing each feature
    vector's true classification:
    [1, 1, 0, ...]
  """
  def setup_feature_vectors(self, pos_class_name, f_vectors_classnames):
    result_f_vectors = []
    y = []

    for f_vector_classname in f_vectors_classnames:
      f_vector = f_vector_classname[0]
      y_true = f_vector_classname[1]

      # Separate the feature vector from its labelled class_name
      result_f_vectors.append(f_vector)

      # Re-mapping classnames to positive or negative classes
      if y_true == pos_class_name:
        y.append(1) # because positive
      else:
        y.append(-1) # because all other classes other than pos_class_name are negative

    return [result_f_vectors, y]

#===========================================================================#
# EXECUTING THE PROGRAM
#===========================================================================#
PATH_TO_STOP_WORDS = sys.argv[1]
PATH_TO_TRAIN_CLASS_LIST = sys.argv[2]
PATH_TO_MODEL = sys.argv[3]

print("PATH_TO_STOP_WORDS:", PATH_TO_STOP_WORDS,
      ", PATH_TO_TRAIN_CLASS_LIST:", PATH_TO_TRAIN_CLASS_LIST,
      ", PATH_TO_MODEL", PATH_TO_MODEL)

TextClassifier().build()

# pickle.dump(model, open(PATH_TO_MODEL, 'wb'))
print("=== FINISHED TRAINING...MODEL SAVED IN " + PATH_TO_MODEL + " ===")
