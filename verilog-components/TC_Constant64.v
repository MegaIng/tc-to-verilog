module TC_Constant64(value);
    output [63:0] value;
    
    parameter constant = 64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000;
    
    assign value = constant;
endmodule

