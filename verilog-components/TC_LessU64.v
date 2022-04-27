module TC_LessU64(in0, in1, out);
    input [63:0] in0;
    input [63:0] in1;
    output out;
    
    assign out = in0 < in1;
endmodule

