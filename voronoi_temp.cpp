#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>

#include "headers.h"
using namespace std;

ofstream writer;
ifstream reader;

string recentMapName;

// TERRAIN TILES:
vector<char> terrainTiles = {'n', 'f', '.', '^', '~', ',', '='};   
int stTilov = terrainTiles.size();

// COLOR TILES:
vector<int> colorTiles = {14, 2, 2, 8, 3, 10, 14};

// ustvari seed-e:
int** generateRandomPoints(int** seeds, int nmbSeeds){

    int rX;
    int rY;
    int tile;

    for(int i = 0; i < nmbSeeds; i++){         
            rX = rand() % nmbSeeds;
            rY = rand() % nmbSeeds;
            tile = rand() % stTilov;

            seeds[i][0] = rX;               //  ***
            seeds[i][1] = rY;               //  ***
            seeds[i][2] = tile;             //  ***                                           
    }

    return seeds;
}

//-----------------------VORONOI MAP----------------------------
char** createVoronoiMap(char** worldMap, int** seeds, int dim){

    double min;
    double distance;
    int seedX, seedY;
    bool once = true;
    int type;

    for(int i = 0; i < dim; i++){       // gre čez cel world map
        for(int j = 0; j < dim; j++){
            
            if(worldMap[i][j] == 'X'){
                
                for(int k = 0; k < dim; k++){
                    seedX = seeds[k][0];
                    seedY = seeds[k][1];
                    distance = computeDistance(i,j,seedX,seedY);

                    if(once){
                        min = distance;
                        once = false;
                    }

                    if(distance <= min){
                        min = distance;
                        type = seeds[k][2];   
                    }                       
                }
                worldMap[i][j] = terrainTiles[type];           
            }                     
        }
        once = true;       
    }

    return worldMap;
}

double computeDistance(int pX, int pY, int seedX, int seedY){
    double distance;

    distance = sqrt(pow((pX - seedX), 2) + pow((pY - seedY), 2));
    return distance;
}

//-----------------------------------------------------------------

int generateWMap(int dim, int slvl, string name){

    // World map and save file naming:
    string path = "C:\\Users\\Matevzv\\Desktop\\YearZero\\worlds\\";
    string ending = ".txt";
    name = name + ending;
    name = path + name;

    //---------CREATION OF WORLD MAP 2D ARRAY--------
    char** worldMap;
    worldMap = new char*[dim];

    for(int i = 0; i < dim; i++){
        worldMap[i] = new char[dim];
    }
    // napolni world map z znaki X:
    for(int i = 0; i < dim; i++){
        for(int j = 0; j < dim; j++){
            worldMap[i][j] = 'X';
        }
    }
    //------------------------------------------------
    
    //--------CREATION OF SEEDS ARRAY-----------------
    int nmbSeeds = dim;
    int** seeds;
    seeds = new int*[nmbSeeds];
    for(int i = 0; i < nmbSeeds; i++){
        seeds[i] = new int[3];             // spremeni dolzino stolpcev, v primeru, da je seeds tabela vecja kot dim x 3 (3: [x,y,type]) SPREMENI TUDI PRI KOMENTRAJU ***
    }
    //------------------------------------------------

    seeds = generateRandomPoints(seeds, nmbSeeds);
    
    // Fills world map with created seeds:
    for(int i = 0; i < nmbSeeds; i++){
        worldMap[seeds[i][0]][seeds[i][1]] = terrainTiles[seeds[i][2]];
    }

    worldMap = createVoronoiMap(worldMap,seeds,dim);

    // Sets map name for later start:
    setRecentMapName(name);
    
    // Writes the map to a file:
    writer.open(name);

    for(int i = 0; i < dim; i++){
        for(int j = 0; j < dim; j++){
            writer << worldMap[i][j];
        }
        writer << endl;
    }

    writer.close();  

    return 0;
}


// SETTERS & GETTERS:

vector<int> getColorTiles(){
    return colorTiles;
}

vector<char> getTerrainTiles(){
    return terrainTiles;
}

int getStTilov(){
    return stTilov;
}

void setRecentMapName(string name){
    recentMapName = name;
}

string getRecentMapName(){
    return recentMapName;
}