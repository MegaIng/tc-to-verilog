module TC_ProgramWord (clk, rst, address, out0, out1, out2, out3);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEXFILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [15:0] address;
    output reg [BIT_WIDTH-1:0] out0;
    output reg [BIT_WIDTH-1:0] out1;
    output reg [BIT_WIDTH-1:0] out2;
    output reg [BIT_WIDTH-1:0] out3;

    reg [15:0] address_reg;
    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];

    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs(ARG_SIG, hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end
        address_reg <= 16'h0000;
    end

    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out0 <= {BIT_WIDTH{1'b0}};
            out1 <= {BIT_WIDTH{1'b0}};
            out2 <= {BIT_WIDTH{1'b0}};
            out3 <= {BIT_WIDTH{1'b0}};
            address_reg <= 16'h0000;
        end else begin
            out0 <= mem[address_reg];
            out1 <= mem[address_reg+1];
            out2 <= mem[address_reg+2];
            out3 <= mem[address_reg+3];
        end
    end
    
    always @ (negedge clk) begin
        if (!rst) begin
            address_reg <= address;
        end
    end
endmodule

