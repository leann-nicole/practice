//querying a mysql database using C++
#include <iostream>
#include <string>
#include <mysql/mysql.h> //found in /usr/include/mysql
using namespace std;

class ConnDetails{
	public:
	
		char* server; 	//localhost
		char* user;   	//root
		char* password;	
		char* database;
		
		ConnDetails(char* s, char* u, char* p, char* d): server(s), user(u), password(p), database(d){}
};

MYSQL* connect(ConnDetails cd){
	MYSQL* connection = mysql_init(NULL); 
	
	if(!mysql_real_connect(connection, cd.server, cd.user, cd.password, cd.database, 0, NULL, 0)){ 
		cout<<"There was a connection error: "<<mysql_error(connection)<<endl;
		exit(1);
	}
	return connection;
}

MYSQL_RES* query(MYSQL* connection, char* query){
	if(mysql_query(connection, query)){ //returns 0 if succeeds
		cout<<"Query failed: "<<mysql_error(connection)<<endl;
		exit(1);
	}
	return mysql_use_result(connection);
}

int main(){
	MYSQL* connection;
	MYSQL_RES* qresult;
	MYSQL_ROW row;
	
	ConnDetails cd("localhost","root","","wellfit");
	
	connection = connect(cd);
	
	char* q;
	string sq;
	char choice;	
	
	while(true){
		
		
		cout<<"Query: ";
		getline(cin,sq);
		q = const_cast<char*>(sq.c_str());
		
		qresult = query(connection,q);
		
		
		while(row = mysql_fetch_row(qresult)){
			cout<<row[0]<<' '<<row[1]<<' '<<row[2]<<' '<<row[3]<<' '<<row[4]<<endl;
		}
		
		cout<<"Again? y/n : ";
		cin>>choice;
		if(choice == 'n')break;
		cin.ignore();
	}
	mysql_free_result(qresult);
	mysql_close(connection);	
	
	return 0;
}
