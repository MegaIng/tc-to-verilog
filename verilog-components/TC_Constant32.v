module TC_Constant32(value);
    output [31:0] value;
    
    parameter constant = 32'b0000_0000_0000_0000_0000_0000_0000_0000;
    
    assign value = constant;
endmodule

