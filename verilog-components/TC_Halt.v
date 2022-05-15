module TC_Halt (clk, rst, en);
    parameter UUID = 0;
    parameter NAME = "";
    parameter HALT_MESSAGE = "";
    input clk;
    input rst;
    input en;
    
    always @ (negedge clk) begin
        if (en) begin
            $display(HALT_MESSAGE);
            $stop;
        end
    end
endmodule
