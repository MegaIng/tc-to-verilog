module TC_Equal(in0, in1, out);
    parameter size = 1;
    input [size-1:0] in0;
    input [size-1:0] in1;
    output out;
    
    assign out = (in0 ^ in1) == {size{1'b0}};
endmodule

