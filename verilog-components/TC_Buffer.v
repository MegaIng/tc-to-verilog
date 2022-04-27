module TC_Buffer(in, out);
    parameter size = 1;
    input [size-1:0] in;
    output [size-1:0] out;
    
    assign out = in;
endmodule

