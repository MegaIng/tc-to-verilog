module TC_LessU32(in0, in1, out);
    input [31:0] in0;
    input [31:0] in1;
    output out;
    
    assign out = in0 < in1;
endmodule

