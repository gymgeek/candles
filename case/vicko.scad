fn = 300;
module case(){
    //steny
    difference(){
        cylinder(20,52/2,52/2,$fn=fn);
        translate([0,0,0])cylinder(21,50/2,50/2,$fn=fn);
    }
 
   
    //dno
    difference(){
        cylinder(1,51/2,51/2,$fn=fn);
        translate([-2.5,15,-0.1])cube([5,5,2]);
        rotate([0,0,00])translate([-8,-20,-0.1])cube([13,9,2]);
    }
        
        
}
case();