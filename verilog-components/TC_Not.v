module TC_Not(in, out);
    parameter BIT_WIDTH = 1;
    input [BIT_WIDTH-1:0] in;
    output [BIT_WIDTH-1:0] out;
    
    assign out = ~in;
endmodule

