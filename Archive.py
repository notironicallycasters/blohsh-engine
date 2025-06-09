def render_vertices():
    for v in range(len(vertex_table)):
        x,y,z = vertex_table[v]
        if camera[2] > z:
            continue
        x_p = ((x-camera[0])*focal_length) / ((z-camera[2]))
        y_p = ((y-camera[1])*focal_length) / ((z-camera[2]))

        x_p += width
        y_p += height

        r,g,b = vertex_color
        r = max(min(255,255-int(r*((camera[2]-focal_length)/100))),0)
        g = max(min(255,int(g*((camera[2]-focal_length)/100))),0)
        b = max(min(255,int(b*((camera[2]-focal_length)/100))),0)
            
        circle(x_p,y_p,5,(r,g,b))
        
def render_edges():
    for e in range(len(edge_table)):
        a,b = edge_table[e]
        if camera[2] > vertex_table[a][2] or camera[2] > vertex_table[b][2]:
            continue
        x,y,z = vertex_table[a]
        
        x_p = ((x-camera[0])*focal_length) / ((z-camera[2]))
        y_p = ((y-camera[1])*focal_length) / ((z-camera[2]))
        x_p += width
        y_p += height
        a_p = (x_p,y_p)

        x,y,z = vertex_table[b]
        x_p = ((x-camera[0])*focal_length) / ((z-camera[2]))
        y_p = ((y-camera[1])*focal_length) / ((z-camera[2]))
        x_p += width
        y_p += height
        b_p = (x_p,y_p)

        r,g,b = edge_color
        g = max(min(255,g-int(g*(z/100))),0)
        line(a_p,b_p,edge_width,edge_color)