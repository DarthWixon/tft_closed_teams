#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <string>

class BaseClass{
private:
public:
	std::map<std::string, int> origin_dict = {
	{"cloud", 0},
	{"crystal", 1},
	{"desert", 2},
	{"electric", 3},
	{"glacial", 4},
	{"inferno", 5},
	{"light", 6},
	{"mountain", 7},
	{"ocean", 8},
	{"poison", 9},
	{"shadow", 10},
	{"steel", 11},
	{"woodland", 12},
	{"lunar", 13}
	};

	std::map<std::string, int> role_dict = {
		{"alchemist", 0},
		{"assassin", 1},
		{"avatar", 2},
		{"beserker", 3},
		{"blademaster", 4},
		{"druid", 5},
		{"mage", 6},
		{"mystic", 7},
		{"predator", 8},
		{"ranger", 9},
		{"summoner", 10},
		{"warden", 11},
		{"soulbound", 12}
	};

	std::vector<int> min_origin_array = {2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 2, 3, 2};
	std::vector<int> min_role_array = {1, 3, 1, 3, 2, 2, 3, 2, 3, 2, 3, 2, 2};
	int n_origins = origin_dict.size();
	int n_roles = role_dict.size();
	bool OriginTester(std::vector<int> origin_array)
	{
		for(int i = 0; i < origin_array.size(); i++)
		{	
			int elem = origin_array[i];
			if((elem < min_origin_array[i]) && (elem != 0))
			{
				return false;
			}
		}
		return true;
	}

	bool RoleTester(std::vector<int> role_array)
	{
		for(int i = 0; i < role_array.size(); i++)
		{	
			int elem = role_array[i];
			if((elem < min_role_array[i]) && (elem != 0))
			{
				return false;
			}
		}
		return true;
	}

	bool TeamTester(std::vector<int> origin_array, std::vector<int> role_array)
	{
		return (RoleTester(role_array) && OriginTester(origin_array));
	}
};


class Unit: public BaseClass{
private: 
public:
	std::string name;
	std::vector<int> origin_array;
	std::vector<int> role_array;
	Unit(std::string name_in, std::vector<std::string> origin_list_in ,std::vector<std::string> role_list_in)
	{
		name = name_in;
		origin_array = std::vector<int> (n_origins, 0);
		role_array = std::vector<int> (n_roles, 0);
		for(std::string role : role_list_in)
		{
			if(role == "avatar")
			{
				role_array[role_dict["avatar"]] ++;
				for(std::string origin_string : origin_list_in)
				{
					origin_array[origin_dict[origin_string]] += 2;
				}
			}
			else
			{
				role_array[role_dict[role]] ++;
				for(std::string origin_string : origin_list_in)
				{
					origin_array[origin_dict[origin_string]] += 1;
				}
			}
		}
	}
	~Unit(){}
};

class Team: public BaseClass{
private: 
public: 
	int n_units = 0;
	std::vector<int> origin_array;
	std::vector<int> role_array;
	std::vector<std::string> team_members;
	bool b_has_lux = false;
	bool b_has_qiyana = false;
	bool b_is_closed = false;
	const int max_max_units = 9;
	std::vector<std::string> qiyana_list = {"Cloud Qiyana", "Inferno Qiyana", "Ocean Qiyana", "Mountain Qiyana"};
	Team()
	{
		origin_array = std::vector<int> (n_origins, 0);
		role_array = std::vector<int> (n_roles, 0);
	};

	void AddUnit(Unit unit)
	{
		if(n_units > max_max_units)
		{
			return;
		}
		else if(std::find(team_members.begin(),team_members.end(), unit.name) != team_members.end())
		{
			return;
		}
		else
		{
			n_units ++;
			for(int i = 0; i < origin_array.size(); i++)
			{
				origin_array[i] += unit.origin_array[i];
			}
			for(int i = 0; i < role_array.size(); i++)
			{
				role_array[i] += unit.role_array[i];
			}
			team_members.push_back(unit.name);
			if(std::find(qiyana_list.begin(), qiyana_list.end(), unit.name) != qiyana_list.end())
			{
				b_has_qiyana = true;
			}
			b_has_lux |= unit.role_array[role_dict["avatar"]]; // or eq 
		}
	}

	void TestTeam(void)
	{
		b_is_closed = TeamTester(origin_array, role_array);
	}

	void PrintReport(void)
	{
		TestTeam();
		if(b_is_closed)
		{
			std::cout << "This is a closed team of size " << n_units << ": ";
			for(auto thing: team_members)
			{
				std::cout << thing << ", ";
			} 
			std::cout << std::endl;
		}
		else
		{
			std::cout << "This is not a closed team." << std::endl;
		}
	}

	bool MachineReport(void)
	{
		TestTeam();
		return b_is_closed;
	}

	void WipeTeam(void)
	{
		n_units = 0;
		origin_array = std::vector<int> (14,0);
		role_array = std::vector<int> (13,0);
		team_members.resize(0);
		b_has_lux = false;
		b_has_qiyana = false;
		b_is_closed = false;
	}
};

int main()
{
	Unit thresh{"Thresh", {"ocean"}, {"warden"}};
	Unit nautilus{"Nautilus", {"ocean"}, {"warden"}};

	Team test_team;
	std::cout << "Adding Thresh" << std::endl;
	test_team.AddUnit(thresh);
	test_team.PrintReport();
	std::cout << "Adding Nautilus" << std::endl;
	test_team.AddUnit(nautilus);
	test_team.PrintReport();
	return 0;
}