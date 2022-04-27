module TC_ByteConstant(value);
    output [7:0] value;
    
    parameter constant = 8'b0000_0000;
    
    assign value = constant;
endmodule

