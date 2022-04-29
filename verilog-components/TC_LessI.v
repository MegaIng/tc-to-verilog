module TC_ByteLessI(in0, in1, out);
    parameter BIT_WIDTH = 1;
    input signed [BIT_WIDTH-1:0] in0;
    input signed [BIT_WIDTH-1:0] in1;
    output out;
    
    assign out = in0 < in1;
endmodule

