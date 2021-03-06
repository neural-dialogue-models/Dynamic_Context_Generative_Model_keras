from keras.layers import Input, LSTM, Embedding, Dense, concatenate, Reshape, SimpleRNN
from keras.models import Model
from keras.utils import plot_model
import numpy as np
from data import DataPreparation
import keras
from keras.models import load_model

# data prep
word_dim = 4000
unknown_token = "UNKNOWN_TOKEN"
sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"

# NN params
fnn_hidden_dim = 2000
len_context = 4000
fnn_output_dim = 4000
len_sentence = 4000
rnn_hidden_dim = 2000
output_dim = 4000
epochs = 2

print("Data Preparation Begins")
data = DataPreparation(word_dim, sentence_start_token, sentence_end_token, unknown_token)
context, message, response = data.data_preprocessing()
index = int((len(context))/3)
context, context_test = context[:index].reshape(len(context[:index]), len_context, 1), context[index+1:].reshape(len(context[index+1:]), len_context, 1)
message, message_test = message[:index].reshape(len(message[:index]), len_context, 1), message[index+1:].reshape(len(message[index+1:]), len_context, 1)
response, response_test = response[:index], response[index+1:]
c_m_combined = context + message
print("Data Preparation Ends")
print("shape: context", context.shape, "shape: context", message.shape, "shape: response", response.shape)

main_input = Input(shape=(len_context, 1), dtype='float32', name='main_input')
x = Embedding(output_dim=fnn_hidden_dim, input_dim=len_context, input_length=len_context)(main_input)
fnn_hidden = Dense(1, activation='relu')(x)
auxiliary_input = Input(shape=(len_context, 1), name='aux_input')
x = SimpleRNN(10)(keras.layers.add([fnn_hidden, auxiliary_input]))
main_output = Dense(output_dim, activation='softmax')(x)
model = Model(inputs=[main_input, auxiliary_input], outputs=main_output)
model.compile(optimizer='adam', loss='binary_crossentropy')
model.fit([c_m_combined, message], response, epochs=epochs)
plot_model(model, to_file='model.png')
model.save('model.h5')
result = model.evaluate([context_test.reshape(len(context), len_context, 1), message_test.reshape(len(context), len_context, 1)], response_test)
print(result)

pred = model.predict([context_test[10].reshape(1, len_context, 1), message_test[10].reshape(1, len_context, 1)], response_test[10])
print(pred)