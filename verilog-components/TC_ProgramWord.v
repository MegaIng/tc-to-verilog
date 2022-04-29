module TC_ProgramWord (clk, rst, address, out0, out1, out2, out3);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 65536;
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [15:0] address;
    output reg [7:0] out0;
    output reg [7:0] out1;
    output reg [7:0] out2;
    output reg [7:0] out3;

    reg [BIT_WIDTH:0] mem [0:MEM_WORDS];

    initial begin
        if ($value$plusargs("HEXFILE=%s", hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end
    end

    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out0 <= {BIT_WIDTH{1'b0}};
            out1 <= {BIT_WIDTH{1'b0}};
            out2 <= {BIT_WIDTH{1'b0}};
            out3 <= {BIT_WIDTH{1'b0}};
        end else begin
            out0 <= mem[address];
            out1 <= mem[address+1];
            out2 <= mem[address+2];
            out3 <= mem[address+3];
        end
    end
endmodule

