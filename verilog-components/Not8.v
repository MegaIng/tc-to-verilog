module TC_Not8(in, out);
    input [7:0] in;
    output [7:0] out;
    
    assign out = ~in;
endmodule

