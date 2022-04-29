module TC_On(value);
    parameter BIT_WIDTH = 1;
    output value;
    
    assign value = {BIT_WIDTH{1'b1}};
endmodule

