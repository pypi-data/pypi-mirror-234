import numpy as np

class SimpleNeuralNetwork:
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size)
        self.bias = np.zeros((1, output_size))

    def forward(self, inputs):
        return np.dot(inputs, self.weights) + self.bias

    def train(self, inputs, targets, learning_rate=0.01, epochs=1000):
        print("Training:")
        for epoch in range(epochs):
            # Forward pass
            predictions = self.forward(inputs)

            # Calculate the mean squared error
            error = np.mean((predictions - targets) ** 2)

            # Backward pass
            derror_doutput = 2 * (predictions - targets) / len(targets)
            doutput_dweights = inputs.T
            derror_dweights = np.dot(doutput_dweights, derror_doutput)
            derror_dbias = np.sum(derror_doutput, axis=0, keepdims=True)

            # Update weights and bias
            self.weights -= learning_rate * derror_dweights
            self.bias -= learning_rate * derror_dbias

            # Print the loss for every 100 epochs
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {error}")

        print("Training completed.")


