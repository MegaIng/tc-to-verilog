module TC_Constant16(value);
    output [15:0] value;
    
    parameter constant = 16'b0000_0000_0000_0000;
    
    assign value = constant;
endmodule

