module TC_Halt (en);
    input en;
    
    always @ (posedge en)
        $stop;
endmodule
