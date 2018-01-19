CXX=g++
CXXFLAGS= -Wall -std=c++14 -I /usr/local/Aria/include -L/usr/local/Aria/lib
LDFLAGS= -lAria
SRC= main.cpp algorithm.cpp utils.cpp

OBJ= $(SRC:%.cpp=%.o)
EXECUTABLE= robot

all: $(OBJ) $(EXECUTABLE)

$(EXECUTABLE):
	$(CXX) $(CXXFLAGS) -o $@ $(OBJ) $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	$(RM) robot *.o
