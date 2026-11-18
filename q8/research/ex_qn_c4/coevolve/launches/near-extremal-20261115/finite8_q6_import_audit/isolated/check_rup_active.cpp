// Independent RUP checker with proof deletions for learned clauses.
// Original axioms are retained. Deleting consequences is logically optional.
// Every added clause is checked against only earlier active consequences.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Clause {vector<int>lit;int a=0,b=1;bool original=false,active=true;};
struct Checker {
 int nv;vector<Clause>cs;vector<vector<int>>watch;vector<int>units,assignment,queue,used;
 unordered_multimap<unsigned long long,int>lookup;
 Checker(int n):nv(n),watch(2*n+2),assignment(n+1){}
 int ix(int lit){return 2*(abs(lit)-1)+(lit<0);}
 int value(int lit){return assignment[abs(lit)]*(lit>0?1:-1);}
 bool enqueue(int lit){int v=value(lit);if(v<0)return false;if(!v){assignment[abs(lit)]=lit>0?1:-1;queue.push_back(lit);}return true;}
 static unsigned long long hash(const vector<int>&v){unsigned long long h=1469598103934665603ULL;for(int l:v){h^=unsigned(l);h*=1099511628211ULL;}return h;}
 bool rup(const vector<int>&clause){
  fill(assignment.begin(),assignment.end(),0);queue.clear();used.clear();
  for(int lit:clause)if(!enqueue(-lit))return true;
  for(int id:units)if(cs[id].active){if(value(cs[id].lit[0])<=0)used.push_back(id);if(!enqueue(cs[id].lit[0]))return true;}
  for(size_t head=0;head<queue.size();head++){
   int f=-queue[head];auto &list=watch[ix(f)];size_t k=0;
   while(k<list.size()){
    int id=list[k];auto &c=cs[id];
    if(!c.active){list[k]=list.back();list.pop_back();continue;}
    int *wf=c.lit[c.a]==f?&c.a:&c.b;int other=wf==&c.a?c.b:c.a;
    if(c.lit[*wf]!=f){cerr<<"internal watcher error\n";exit(3);}
    if(value(c.lit[other])>0){k++;continue;}
    int replacement=-1;
    for(int j=0;j<int(c.lit.size());j++)if(j!=c.a&&j!=c.b&&value(c.lit[j])>=0){replacement=j;break;}
    if(replacement>=0){*wf=replacement;list[k]=list.back();list.pop_back();watch[ix(c.lit[replacement])].push_back(id);}
    else{if(value(c.lit[other])<=0)used.push_back(id);if(!enqueue(c.lit[other]))return true;k++;}
   }
  }return false;
 }
 void add(vector<int>v,bool original=false){
  sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());
  for(int l:v){if(abs(l)>nv||!l)exit(4);if(binary_search(v.begin(),v.end(),-l))return;}
  if(v.empty())return;
  int id=cs.size();cs.push_back({move(v),0,1,original,true});lookup.emplace(hash(cs[id].lit),id);
  if(cs[id].lit.size()==1)units.push_back(id);
  else{watch[ix(cs[id].lit[0])].push_back(id);watch[ix(cs[id].lit[1])].push_back(id);}
 }
 void remove(vector<int>v){
  sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());
  auto range=lookup.equal_range(hash(v));
  for(auto it=range.first;it!=range.second;++it){auto &c=cs[it->second];if(!c.original&&c.lit==v)c.active=false;}
 }
 bool has_active(const vector<int>&v){auto range=lookup.equal_range(hash(v));for(auto it=range.first;it!=range.second;++it)if(cs[it->second].active&&cs[it->second].lit==v)return true;return false;}
};
int main(int argc,char**argv){
 if(argc!=3)return 2;auto start=chrono::steady_clock::now();ifstream in(argv[1]);string line;int nv=0,expected=0;vector<vector<int>>input;
 while(getline(in,line)){if(line.empty()||line[0]=='c')continue;istringstream s(line);if(line[0]=='p'){string p,t;s>>p>>t>>nv>>expected;continue;}vector<int>c;int l;bool end=false;while(s>>l){if(!l){end=true;break;}c.push_back(l);}if(!end)return 5;input.push_back(c);}
 if(nv<=0||int(input.size())!=expected)return 6;Checker checker(nv),history(nv);for(auto c:input){checker.add(c,true);history.add(c,true);}
 ifstream proof(argv[2]);if(!proof)return 7;long long additions=0,deletions=0,linenumber=0,fallbacks=0,restored=0;bool empty=false;
 while(getline(proof,line)){
  linenumber++;if(line.empty()||line[0]=='c')continue;bool del=line[0]=='d';istringstream s(del?line.substr(1):line);vector<int>c;int l;bool end=false;
  while(s>>l){if(!l){end=true;break;}if(abs(l)>nv)return 8;c.push_back(l);}if(!end)return 9;
  if(del){checker.remove(c);deletions++;continue;}
  if(!checker.rup(c)){
   fallbacks++;
   // The complete historical store contains ORIGINAL AXIOMS and only
   // STRICTLY EARLIER checked additions. It never contains this C yet.
   if(!history.rup(c)){cerr<<"NOT RUP at line "<<linenumber<<" addition "<<additions+1<<'\n';return 1;}
   // Every restored reason is already a proved consequence. Restore only
   // propagation reasons, leaving the active database small. Copies are
   // freshly attached, avoiding stale-watch reactivation.
   for(int id:history.used)if(!checker.has_active(history.cs[id].lit)){checker.add(history.cs[id].lit);restored++;}
  }
  additions++;if(c.empty()){empty=true;break;}checker.add(c);history.add(c);
 }
 cout<<"{\"valid\":"<<(empty?"true":"false")<<",\"verified_additions\":"<<additions<<",\"processed_deletions\":"<<deletions<<",\"history_fallbacks\":"<<fallbacks<<",\"restored_prior_reasons\":"<<restored<<",\"final_empty_clause\":"<<(empty?"true":"false")<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
 return empty?0:10;
}
