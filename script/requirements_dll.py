import seaborn as sns
import pm4py
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import tensorflow as tf
from tensorflow import keras
from scipy.optimize import fmin
from tensorflow.keras.models import Model
from tensorflow.keras import activations, regularizers
from tensorflow.keras.layers import Input, Dense, BatchNormalization, LSTM, Softmax, Dropout, RepeatVector, Concatenate, Masking, TimeDistributed, Embedding, Flatten, Reshape, SimpleRNN, GRU
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import confusion_matrix, log_loss, f1_score
from sklearn.utils.class_weight import compute_class_weight
sns.set()

def print_model_results(model):
    fig, (ax1) = plt.subplots(1, 1, figsize =(5,4))
    ax1.plot(history.history['loss'])
    ax1.plot(history.history['val_loss'])
    ax1.set_title('Model Loss')
    ax1.set_ylabel('Loss')
    ax1.set_xlabel('Epoch')
    ax1.legend(['Train', 'Validation'], loc = 'upper right')
    plt.savefig(name+'_plot.pdf', bbox_inches = 'tight')
    plt.show()

    T5_labels = onehot_encoder_act.inverse_transform(np.identity(n_act))[:,0]
    cm = confusion_matrix(y_test.argmax(axis = 1), yhat.argmax(axis = 1), labels = np.identity(n_act).argmax(axis = 1), normalize = 'true')
    df_cm = pd.DataFrame(cm, range(n_act), range(n_act))
    sns.set(font_scale = 3.4)
    g = sns.heatmap(df_cm, annot = True, annot_kws={'size' : 10},
                    xticklabels= T5_labels, yticklabels= T5_labels,
                    vmin = 0, vmax = 1, fmt=".0%", cmap ='Blues',
                    square = True, linewidths=0.4, cbar_kws={"shrink" : .8})
    g.set_xticklabels(g.get_xmajorticklabels(), fontsize = 10)
    g.set_yticklabels(g.get_xmajorticklabels(), fontsize = 10) 
    plt.xticks(rotation=90)
    plt.savefig(name+'_confusion_matrix.pdf', bbox_inches = 'tight')
    plt.show()

def find_max_list(list):
    list_len = [len(i) for i in list]
    return max(list_len)

def one_hot_column(col):
    col_uniq = pd.unique(col)
    n_col_uniq = len(col_uniq)
    onehot_encoder = OneHotEncoder(sparse = False)
    onehot_encoded = onehot_encoder.fit_transform(col_uniq.reshape(-1,1))
    return n_col_uniq, onehot_encoder

def softmax_to_one_hot(y):
    y_copy = y.copy()
    idx = y_copy.argmax(axis = 1)
    for i in range(len(y_copy)):
        y_copy[i, idx[i]] = 1
    y_copy[y_copy != 1] = 0
    return y_copy

def brier_multi(targets,probs):
    return np.mean(np.sum((probs - targets) **2, axis = 1))

def temperature_scaling(y,T):
    y_2 = np.exp(y/T) / np.sum(np.exp(y/T), axis = 1)[:, None]
    return y_2

def find_min_t(T):
    logloss = np.mean(weighted_categorical_crossentropy_comp(class_weights, y_test, temperature_scaling(yhat, T)))
    return logloss


def temperature_scaling_bin(y,T):
    y_2 = 1 / (1 + np.exp(-y/T))
    return y_2


def find_min_t_bin(T):
    logloss = np.mean(keras.metrics.binary_crossentropy(y_mav_test, temperature_scaling_bin(yhat_mavp, T)))
    return logloss

from keras import backend as K
def weighted_categorical_crossentropy(weights):
    
    weights = K.variable(weights)
        
    def loss(y_true, y_pred):
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
        
        y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
        loss = y_true * K.log(y_pred) * weights
        loss = -K.sum(loss, -1)
        return loss
    
    return loss

from keras import backend as K
def weighted_categorical_crossentropy_comp(weights, y_true, y_pred):
    
    weights = weights.astype('float32')
    y_true = y_true.astype('float32')
    y_pred = y_pred.astype('float32')

    weights = K.variable(weights)
    y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
    
    y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
    loss = y_true * K.log(y_pred) * weights
    loss = -K.sum(loss, -1)
    return loss

def weighted_binary_crossentropy(zero_weight, one_weight):

    def weighted_binary_crossentropy(y_true, y_pred):

        b_ce = K.binary_crossentropy(y_true, y_pred)

        weight_vector = y_true * one_weight + (1 - y_true) * zero_weight
        weighted_b_ce = weight_vector * b_ce

        return K.mean(weighted_b_ce)

    return weighted_binary_crossentropy

def weighted_binary_crossentropy_comp(zero_weight, one_weight, y_true, y_pred):
    #weights = weights.astype('float32')
    y_true = y_true.astype('float32')
    y_pred = y_pred.astype('float32')
    b_ce = K.binary_crossentropy(y_true, y_pred)

    # weighted calc
    weight_vector = y_true * one_weight + (1 - y_true) * zero_weight
    weighted_b_ce = weight_vector * b_ce

    return K.mean(weighted_b_ce)