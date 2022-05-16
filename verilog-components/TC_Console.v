module TC_Console (clk, rst, en, data);
    parameter UUID = 0;
    parameter NAME = "";
    input clk;
    input rst;
    input en;
    input [31:0] data;

    always @ (negedge clk) begin : ConsoleOutput
        integer junk;
        if (en) begin
            //$write("%c", data[7:0]);
            junk = $fputc(data[7:0], 32'h8000_0001);
        end
    end
endmodule