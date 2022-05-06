module TC_On(value);
    parameter UUID = 0;
    parameter NAME = "";
    parameter BIT_WIDTH = 1;
    output value;
    
    assign value = {BIT_WIDTH{1'b1}};
endmodule

