module TC_LessU16(in0, in1, out);
    input [15:0] in0;
    input [15:0] in1;
    output out;
    
    assign out = in0 < in1;
endmodule

