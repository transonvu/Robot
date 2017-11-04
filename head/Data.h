#ifndef DATA
#define DATA

typedef void(*Action)();

class Data {
private:
	static Data* sharedInstance;

	Action chActions[24];
	Action numActions[10];
public:
	static Data* getInstance();
	void addAction(char key, Action action);
	Action act(char key);
};

#endif
