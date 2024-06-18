i = 0
while i < 9:
    i += 1
    if i == 3:
        print("continuing")
        continue
    
    print(i)


def Astar(ySlice, start, end):

    # written with reference to https://youtu.be/-L-WgKMFuhE?si=UlBWzKz5x3yjQHLc&t=455
    # ySlice is the slice of the 3D array
    # start [x,y,z]
    # end [x,y,z]

    openList = [] # [x,y,z,f,g,h,parent]
    closedList = []
    blank = 0,0,0
    path = []

    # debug
    # start = 1,0,1
    # end = 3,0,9 
    # ySlice = [[0,0,0,0,0,0,0,0,0,0,0]
    #          ,[0,0,0,0,0,0,0,1,1,0,0]
    #          ,[0,0,1,1,1,1,1,1,1,0,0]
    #          ,[0,0,1,0,0,0,1,1,1,0,0]
    #          ,[0,0,0,0,0,0,0,0,0,0,0]
    #          ,[0,0,0,0,0,0,0,0,0,0,0]]
    
    # add the start node to the open list
    openList.append([int(start[0]),int(start[1]),int(start[2]),0,0,0,blank])


    while openList:
        
        # sort list by lowest f value 
        openList.sort(key=lambda x: x[3])


        # set current node from the open list
        current = openList[0]
        # remove the current node from the open list
        openList.remove(current)
        # add the current node to the closed list
        closedList.append(current)

        # check if the current node is the end node
        if current[0] == end[0] and current[1] == end[1] and current[2] == end[2]:
            print("path found")
            # generate the path
            if current[0] == end[0] and current[1] == end[1] and current[2] == end[2]:
                path.append([current[0],current[1],current[2]])
                
                # search for the coordinates in closedList and then set the closed list item as the current node
                for item in closedList:
                    if item[0] == current[6][0] and item[1] == current[6][1] and item[2] == current[6][2]:
                        path.append([item[0],item[1],item[2]])
                        current = item

            while closedList:
                for item in closedList:
                    if item[0] == current[6][0] and item[1] == current[6][1] and item[2] == current[6][2]:
                        path.append([item[0],item[1],item[2]])
                        current = item
                
                if current[0] == start[0] and current[2] == start[2]:
                    #print(closedList)    
                    return path
        
        # generate the children of the current node
        for i in range(-1,2):
            for j in range(-1,2):
                # check if the child is the current node
                try:
                    if i == 0 and j == 0:
                        continue
                    # ensure coordinates are not negative
                    if int(current[0])+i < 0 or int(current[2]+j) < 0:
                        continue

                    # check if the child is collidable
                    if ySlice[int(current[0])+i][int(current[2]+j)] == 1:                
                        continue

                    # check if the child is within the bounds of the grid
                    if ySlice[int(current[0])+i][int(current[2]+j)] != 0:
                        continue

                    # check if the child is in the closed list
                    tolerance = 0
                    for block in closedList:
                        if block[0] == int(current[0])+i and block[2] == int(current[2]+j):
                            tolerance += 1
                            continue
                    if tolerance >= 1:
                        continue

                    # check if the child is in the open list
                    tolerance = 0
                    for block in openList:
                        if block[0] == int(current[0])+i and block[2] == int(current[2]+j):
                            tolerance += 1
                            continue
                    if tolerance >= 1:
                        continue
                    
                except IndexError:
                    continue

                # calculate the f,g,h values
                g = current[4] + sqrt(i**2 + j**2)
                h = sqrt((current[0]+i-end[0])**2 + (current[2]+j-end[2])**2)
                f = (g*10) + (h*10)
                parent = current[0],current[1],current[2]

                # add the child to the open list
                #print("child: " + str([int(current[0])+i,current[1],int(current[2]+j),f,g,h,parent]))
                openList.append([int(current[0])+i,current[1],int(current[2]+j),f,g,h,parent])