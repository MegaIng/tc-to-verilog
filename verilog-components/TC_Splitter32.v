module TC_Splitter32 (in, out0, out1, out2, out3);
    input [31:0] in;
    output [7:0] out0;
    output [7:0] out1;
    output [7:0] out2;
    output [7:0] out3;
    
    assign {out3, out2, out1, out0} = in;
endmodule

