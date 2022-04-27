module TC_Xnor(a, b, out);
    input a;
    input b;
    output out;
    
    assign out = a ~^ b;
endmodule

