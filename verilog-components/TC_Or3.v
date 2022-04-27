module TC_Or3(in0, in1, in2, out);
    parameter size = 1;
    input [size-1:0] in0;
    input [size-1:0] in1;
    input [size-1:0] in2;
    output [size-1:0] out;
    
    assign out = in0 | in1 | in2;
endmodule

