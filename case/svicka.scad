fn = 300;
height = 80;
module case(){
    //steny
    difference(){
        cylinder(height,49/2,49/2,$fn=fn);
        translate([0,0,0])cylinder(100,46/2,46/2,$fn=fn);
    }
 
   
    //dno
    difference(){
        cylinder(1,48/2,48/2,$fn=fn);
        rotate([0,0,30])translate([-8,12,-0.1])cube([10,7,2]);
        
    }
        
        
}
module nodemcuhold(){
  //drazky na nodemcu
    difference(){
        translate([-24,-4,0])cube([48,8,height]);
        translate([-12,-4,0])cube([24,8,height]);
        translate([-17,-2,0])cube([34,4,height]);
        
    }
    *translate([-15,-1,0])cube([30,2,95]); //nodemcu  
}

module powermoduleshold(){
    rotate([0,0,30])translate([-3,15,0]){
    difference(){
        translate([-12,-4,0])cube([24,8,height]);
        translate([-7,-4,0])cube([14,8,height]);
        translate([-9,-2,0])cube([18,4,height]);
        
    }}
    translate([-22,4,0])cube([2.5,2.8,height]);
    
}

module accelerometerhold(){
    rotate([0,0,-35])translate([3,16,0]){
    difference(){
        translate([-13,-4,0])cube([24,8,height]);
        translate([-8,-4,0])cube([14,8,height]);
        translate([-10,-2,0])cube([18,4,height]);
        
    }}
    translate([-1.5,16.5,0])cube([5,7,height]);
    translate([20,4,0])cube([2,2,height]);
   
}
module bat18650(){
    translate([0,15,0])cylinder(65,10,10,$fn=fn);
}


case();
nodemcuhold();
*bat18650();
powermoduleshold();
accelerometerhold();

