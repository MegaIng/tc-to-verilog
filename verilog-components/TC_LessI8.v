module TC_ByteLessI(in0, in1, out);
    input signed [7:0] in0;
    input signed [7:0] in1;
    output out;
    
    assign out = in0 < in1;
endmodule

