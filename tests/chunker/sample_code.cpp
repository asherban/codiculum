#include <iostream>

// A simple function
int add(int a, int b) {
    // Check for positive numbers
    if (a > 0 && b > 0) {
        return a + b; // Add them
    }
    return 0; // Return 0 otherwise
}

// A simple class
class MyClass {
public:
    int value;

    MyClass(int v) : value(v) {}

    void printValue() {
        std::cout << "Value: " << value << std::endl;
    }
};

int main() {
    MyClass obj(10);
    obj.printValue();
    int sum = add(5, 3);
    std::cout << "Sum: " << sum << std::endl;
    return 0;
} 