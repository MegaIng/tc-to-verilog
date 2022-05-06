module TC_Halt (en);
    parameter UUID = 0;
    parameter NAME = "";
    input en;
    
    always @ (posedge en)
        $stop;
endmodule
