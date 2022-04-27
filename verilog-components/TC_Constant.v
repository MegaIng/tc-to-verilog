module TC_Constant(out);
    parameter size = 1;
    parameter value = {size{1'b0}};
    output [size-1:0] out;
    
    assign out = value;
endmodule

