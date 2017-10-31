#include "Data.h"
#include <ctype.h>

Data* Data::sharedInstance = 0;

Data* Data::getInstance() {
	if (sharedInstance == 0) {
		sharedInstance = new Data();
	}
	return sharedInstance;
}

void Data::addAction(char key, Action action) {
	key = tolower(key);
	if (key >= 'a' && key <= 'z') {
		chActions[key - 'a'] = action;
	}
	if (key >= '0' && key <= '9') {
		numActions[key - '0'] = action;
	}
}

Action Data::act(char key) {
	key = tolower(key);
	if (key >= 'a' && key <= 'z') {
		return chActions[key - 'a'];
	}
	if (key >= '0' && key <= '9') {
		return numActions[key - '0'];
	}
	return 0;
}
