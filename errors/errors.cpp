#include <iostream>
#include <string>

int foo() {
	int x = 4;
	int y = x * 3;
	std::string z("foo");
	// missing return here
}

int main()
{
	int trash = foo();
	float garbage;
	std::cout << "trash " << trash << ", uninitialized " << garbage << std::endl;
	return 0;
}
